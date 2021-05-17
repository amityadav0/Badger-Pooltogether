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

Rinkeby Network: [0x512E4aB32aA7aB1Bf8B9DDb5b00B099464ECdF4d](https://rinkeby.etherscan.io/address/0x512e4ab32aa7ab1bf8b9ddb5b00b099464ecdf4d)
