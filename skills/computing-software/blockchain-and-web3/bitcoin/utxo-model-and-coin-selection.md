---
id: computing-software.blockchain-and-web3.bitcoin.utxo-model-and-coin-selection
name: utxo-model-and-coin-selection
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [utxo-model, coin-selection, change-output, bc-btc-utxo]
level: intro
status: draft
description: "Understand unspent outputs, inputs spending them, change outputs and coin-selection trade-offs."
sources:
  - https://developer.bitcoin.org/devguide/transactions.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UTXO model
- There are no account balances: a wallet's balance is the sum of its unspent transaction outputs (UTXOs).
- A transaction consumes whole UTXOs as inputs and creates new outputs; anything not paid out becomes change (to a new address) or fee. Inputs minus outputs = fee, so a missing change output donates the difference to miners.
- Coin selection balances fee (more inputs = larger tx), privacy (avoid linking addresses) and dust (outputs below a threshold are non-standard).
- Inspect: `bitcoin-cli listunspent`, `bitcoin-cli gettxout <txid> <n>`.
- Mind the dust limit (relay policy, not consensus).

## Verify
- [ ] For a created transaction, sum(inputs) - sum(outputs) equals the intended fee.
