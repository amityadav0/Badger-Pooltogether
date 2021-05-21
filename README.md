# PoolTogether Badger-WBTC-Vault Yield Source

PoolTogether Yield Source that uses [Badger WBTC Vault](https://etherscan.io/address/0x4b92d19c11435614cd49af1b589001b7c08cd4d5), generates yield by depositing WBTC in Badger-WBTC-Vault.

## Installation

1. `yarn install`

2. This project uses `eth-brownie`, you can install it by following these [instructions])(https://eth-brownie.readthedocs.io/en/stable/install.html)

or 

```
pip install eth-brownie
```

## Test

This project uses [eth-brownie](https://eth-brownie.readthedocs.io/en/stable/index.html) ecosystem to test and deploy

To compile contracts:

```
brownie compile
```

To run tests:

```
brownie test
```

## Deploy

## Setup

You will need enviroment variables to deploy on rinkeby network.

```
export WEB3_INFURA_PROJECT_ID=
export PRIVATE_KEY=
```

You will get the first one from https://infura.io/
You will get the second one from your wallet

To deploy yield source:

```
brownie run scripts/deploy.js --network NETWORK_NAME
```

Note: 
- To deploy the contract on mainnet and have it working you will need to initialize contract with mainnet address of badger-wbtc-vault and address of wbtc token.
- Once it is deployed it will be required to add the yield source contract address in badger-wbtc-vault's guestlist.

## Deployed contract address

Rinkeby Network

- Mock WBTC token: [0x4c679Ed34D4442f8ed439226B0869668D41A5748](https://rinkeby.etherscan.io/address/0x4c679ed34d4442f8ed439226b0869668d41a5748)
- Yearn Token Vault: [0xfe1F35FE85Ca2E9bd3e5c93E13dA14ED29D2B99A](https://rinkeby.etherscan.io/address/0xfe1F35FE85Ca2E9bd3e5c93E13dA14ED29D2B99A)
- Yearn Registry: [0x82E73b83ee46bc09A207Ca7cD886b6dfbf5252d3](https://rinkeby.etherscan.io/address/0x82E73b83ee46bc09A207Ca7cD886b6dfbf5252d3)
- Badger wBTC Vault: [0x8f6A9AAbd9AF782811D3F904a43103c51F77D2bd](https://rinkeby.etherscan.io/address/0x8f6A9AAbd9AF782811D3F904a43103c51F77D2bd)
- Badger wBTC Vault Yield Source: [0xE9C60903B4dE31D2601D3AC00b966AAAe3eAc077](https://rinkeby.etherscan.io/address/0xE9C60903B4dE31D2601D3AC00b966AAAe3eAc077)

- [Here](https://rinkeby.etherscan.io/address/0xbd5a927be6e8da1faf827562779100ce62ed70e5) is are transactions which shows how a end user can deposit and redeem token from yield source contract.
