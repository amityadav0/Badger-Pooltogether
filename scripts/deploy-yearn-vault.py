import os
from brownie import *

def main():
    my_account = accounts.add(os.getenv(config['wallets']['from_key']))
    # accounts created for testing on rinkeby
    random_account1 = "0xbd5a927BE6e8da1faf827562779100ce62eD70E5"
    random_account2 = "0x8a2A2864DAF8175Ed8Ea6FF4f290F0B6E359e2Fe"
    AddressZero = "0x0000000000000000000000000000000000000000"

    # WBTC
    mockToken = MockToken.deploy({'from': my_account})

    print("mock token address", mockToken.address)
    mockToken.initialize(
        [random_account1, random_account2],
        [10e18, 20e18], {'from': my_account}
    )

    governance = accounts.add("")
    # Yearn underlying vault
    vault = YearnTokenVault.deploy({'from': my_account})
    print("Yearn Vault address", vault.address)
    vault.initialize(
        mockToken.address, governance.address, AddressZero, "YearnWBTC", "vyWBTC",
        { 'from': my_account }
    )
    vault.setDepositLimit(24e18, { 'from': governance })

    # Yearn registry
    yearnRegistry = YearnRegistry.deploy({ 'from': governance })
    print("Yearn Registry address", yearnRegistry.address)
    yearnRegistry.setGovernance(governance.address, { 'from': governance })
    # Add vault to registry
    yearnRegistry.newRelease(vault.address, { 'from': governance })
    yearnRegistry.endorseVault(vault.address, { 'from': governance })

    # Deploy and initialize the wrapper contract (deployer -> affiliate)
    badger_wbtc_vault = SimpleWrapperGatedUpgradeable.deploy({ 'from': my_account })
    badger_wbtc_vault.initialize(
        mockToken.address,
        yearnRegistry.address,
        "BadgerYearnWBTC",
        "bvyWBTC",
        my_account.address,
        True,
        vault.address,
        { 'from': my_account }
    )
    print("Badger Vault deployed", badger_wbtc_vault.address)

    # Deploy Yield Source contract
    yield_source = WBTCVaultYieldSource.deploy({ 'from': my_account })
    print("Yield source deployed", yield_source.address)
    yield_source.initialize(badger_wbtc_vault.address, mockToken.address, { 'from': my_account })