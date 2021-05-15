import json
import brownie
import pytest
from brownie import *
from collections import namedtuple

AddressZero = "0x0000000000000000000000000000000000000000"

@pytest.fixture(scope="module", autouse=True)
def setup(
    MockToken, SimpleWrapperGatedUpgradeable,
    YearnTokenVault, YearnRegistry,
    VipCappedGuestListWrapperUpgradeable, WBTCVaultYieldSource):
    # Assign accounts
    deployer = accounts[0]
    affiliate = accounts[1]
    manager = accounts[2]
    guardian = accounts[3]
    randomUser1 = accounts[4]
    randomUser2 = accounts[5]
    randomUser3 = accounts[6]
    distributor = accounts[7]
    yearnGovernance = accounts[8]

    namedAccounts = {
        "deployer": deployer, 
        "affiliate": affiliate, 
        "manager": manager, 
        "guardian": guardian,
        "randomUser1": randomUser1,
        "randomUser2": randomUser2,
        "randomUser3": randomUser3,
        "distributor": distributor,
        "yearnGovernance": yearnGovernance,
    }

    # WBTC (mainnet)
    mockToken = deployer.deploy(MockToken)
    mockToken.initialize(
        [randomUser1.address, randomUser2.address, randomUser3.address, distributor.address],
        [10e18, 20e18, 10e18, 10000e18],
    )

    assert mockToken.balanceOf(randomUser1.address) == 10e18
    assert mockToken.balanceOf(randomUser2.address) == 20e18
    assert mockToken.balanceOf(randomUser3.address) == 10e18

    # Yearn underlying vault
    vault = deployer.deploy(YearnTokenVault)
    vault.initialize(
        mockToken.address, deployer.address, AddressZero, "YearnWBTC", "vyWBTC"
    )
    vault.setDepositLimit(24e18)

    # Yearn registry
    yearnRegistry = deployer.deploy(YearnRegistry)
    yearnRegistry.setGovernance(yearnGovernance)
    # Add vault to registry
    yearnRegistry.newRelease(vault.address)
    yearnRegistry.endorseVault(vault.address)

    # Deploy and initialize the wrapper contract (deployer -> affiliate)
    wrapper = deployer.deploy(SimpleWrapperGatedUpgradeable)
    wrapper.initialize(
        mockToken.address,
        yearnRegistry.address,
        "BadgerYearnWBTC",
        "bvyWBTC",
        guardian.address,
        True,
        vault.address,
    )

    # Deploy Yield Source contract
    yield_source = deployer.deploy(WBTCVaultYieldSource)
    yield_source.initialize(wrapper.address, mockToken.address)

    # Deploy the Guestlist contract (deployer -> bouncer)
    guestlist = deployer.deploy(VipCappedGuestListWrapperUpgradeable)
    guestlist.initialize(wrapper.address)

    # Add users and yield source contract to guestlist
    guestlist.setGuests([randomUser1.address, randomUser2.address, yield_source.address], [True, True, True])
    # Set deposit cap to 15 tokens
    guestlist.setUserDepositCap(15e18)
    guestlist.setTotalDepositCap(50e18)

    yield namedtuple(
        'setup', 
        'mockToken vault yearnRegistry wrapper guestlist namedAccounts yield_source'
    )(
        mockToken, 
        vault,
        yearnRegistry, 
        wrapper, 
        guestlist, 
        namedAccounts,
        yield_source
    )

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_check(setup):
    print("HELLO WORLD")
    assert 1 == 1
    pass

def test_supplyTo(setup):
    randomUser1 = setup.namedAccounts['randomUser1']
    randomUser2 = setup.namedAccounts['randomUser2']
    yieldSourceAddress = setup.yield_source.address

    token = setup.yield_source.depositToken()
    print(token)
    assert token == setup.mockToken.address

    before_balance = setup.yield_source.balanceOfToken(randomUser1.address)
    print(before_balance.events)
    assert before_balance.return_value == 0

    # Approve wrapper as spender of mockToken for users
    setup.mockToken.approve(yieldSourceAddress, 100e18, {"from": randomUser1})
    setup.mockToken.approve(yieldSourceAddress, 100e18, {"from": randomUser2})

    setup.yield_source.supplyTokenTo(1e18, randomUser1, {"from": randomUser1})

    # RandomeUser1 should have balance from yield_source contract
    after_balance = setup.yield_source.balanceOfToken(randomUser1.address)
    print(after_balance)
    assert after_balance.return_value == 1e18

    # tokens should be transfered to badger vault, 
    # and yield source contract must have wrapper balance
    assert setup.wrapper.totalWrapperBalance(yieldSourceAddress) == 1e18

def test_supplyTo_Redeem(setup):
    randomUser1 = setup.namedAccounts['randomUser1']
    randomUser2 = setup.namedAccounts['randomUser2']
    yieldSourceAddress = setup.yield_source.address

    # Approve wrapper as spender of mockToken for users
    setup.mockToken.approve(yieldSourceAddress, 100e18, {"from": randomUser1})
    setup.mockToken.approve(yieldSourceAddress, 100e18, {"from": randomUser2})

    setup.yield_source.supplyTokenTo(1e18, randomUser1, {"from": randomUser1})

    chain.sleep(86400)
    chain.mine(1)

    setup.yield_source.supplyTokenTo(5e18, randomUser2, {"from": randomUser2})


    chain.sleep(86400)
    chain.mine(1)

    val = setup.wrapper.pricePerShare()
    print(val)

    # RandomeUser1 should have balance from yield_source contract
    after_balance = setup.yield_source.balanceOfToken(randomUser1.address)
    print(after_balance)
    assert after_balance.return_value == 1e18

    # RandomeUser2 should have balance from yield_source contract
    balance = setup.yield_source.balanceOfToken(randomUser2.address)
    assert balance.return_value == 5e18

    # tokens should be transfered to badger vault, 
    # and yield source contract must have wrapper balance
    assert setup.wrapper.totalWrapperBalance(yieldSourceAddress) == 6e18

    # Redeem tokens for message sender - Random User
    assert setup.yield_source.balanceOfToken(randomUser1.address).return_value == 1e18
    setup.yield_source.redeemToken(1e18, {"from": randomUser1})

    assert setup.yield_source.balanceOfToken(randomUser1.address).return_value == 0

    chain.sleep(86400)
    chain.mine(1)
    
    # Redeem tokens for message sender - Random User 2
    setup.yield_source.redeemToken(3e18, {"from": randomUser2})

    assert setup.yield_source.balanceOfToken(randomUser2.address).return_value == 2e18

    assert setup.wrapper.totalWrapperBalance(yieldSourceAddress) == 2e18

