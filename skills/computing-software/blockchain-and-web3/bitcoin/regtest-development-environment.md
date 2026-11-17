---
id: computing-software.blockchain-and-web3.bitcoin.regtest-development-environment
name: regtest-development-environment
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [bitcoin-regtest, generatetoaddress, bitcoin-test-wallet]
level: practitioner
status: draft
description: "Use regtest to develop against Bitcoin without real funds: mine blocks, fund addresses and test scenarios."
sources:
  - https://developer.bitcoin.org/examples/testing.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regtest
```
bitcoind -regtest -daemon
bitcoin-cli -regtest createwallet dev
ADDR=$(bitcoin-cli -regtest getnewaddress)
bitcoin-cli -regtest generatetoaddress 101 "$ADDR"   # 101 so the first coinbase matures
bitcoin-cli -regtest getbalance
```
- Blocks are mined instantly on demand; difficulty is minimal.
- Reproduce reorgs with `invalidateblock` / `reconsiderblock`.
- Scripts can drive tests; containers keep state disposable.
- Regtest addresses use the `bcrt1` prefix.

## Verify
- [ ] After 101 blocks, `getbalance` shows a spendable coinbase reward.
