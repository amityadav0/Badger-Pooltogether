import os
from brownie import network, accounts, config, WBTCVaultYieldSource

def main():
    my_account = accounts.add(os.getenv(config['wallets']['from_key']))

    yield_source = WBTCVaultYieldSource.deploy({'from': my_account})

    # WBTC yield source address
    print(yield_source.address)

