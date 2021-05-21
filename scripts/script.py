import os
from brownie import *

def main():
    my_account = accounts.add(os.getenv(config['wallets']['from_key']))
    # these accounts have some tokens already
    randomUser1 = accounts.add("")
    randomUser2 = accounts.add("")

    mockToken = interface.IWBTC("0x4c679Ed34D4442f8ed439226B0869668D41A5748")
    yield_source = interface.IYieldSource("0xE9C60903B4dE31D2601D3AC00b966AAAe3eAc077")

    val = mockToken.balanceOf(randomUser1.address, {'from':my_account})
    val2 = mockToken.balanceOf(randomUser2.address, { 'from': my_account})
    print("Balances: ", val, val2)

    mockToken.approve(yield_source.address, 100e18, {"from": randomUser1})
    mockToken.approve(yield_source.address, 100e18, {"from": randomUser2})

    yield_source.supplyTokenTo(5e18, randomUser1, {"from": randomUser1})
    yield_source.supplyTokenTo(10e18, randomUser1, {"from": randomUser2})

    # RandomeUser1 should have balance from yield_source contract
    after_balance = yield_source.balanceOfToken(randomUser1.address, {'from': my_account})
    print("Random User1 Balance after adding to yield source", after_balance)

    # RandomeUser2 should have balance from yield_source contract
    after_balance = yield_source.balanceOfToken(randomUser2.address, {'from': my_account})
    print("Random User2 Balance after adding to yield source", after_balance)

    # Redeem some tokens from randomuser1
    yield_source.redeemToken(1e18, {"from": randomUser1})
    # RandomeUser1 should have balance from yield_source contract
    after_balance = yield_source.balanceOfToken(randomUser1.address, {'from': my_account})
    print("Random User1 Balance after adding to yield source", after_balance)