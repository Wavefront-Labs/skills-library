---
id: computing-software.blockchain-and-web3.bitcoin.confirmations-and-reorg-risk
name: confirmations-and-reorg-risk
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [confirmations-depth, double-spend-risk, coinbase-maturity]
level: practitioner
status: draft
description: "Pick confirmation depths by value at risk and know coinbase maturity."
sources:
  - https://developer.bitcoin.org/devguide/block_chain.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Confirmations
- 0-conf transactions can be replaced (RBF) or double-spent; fine only for low-value trust-based cases.
- Each additional block makes reversal exponentially harder; commonly 1-6 confirmations are used, scaled to value (a policy choice, not a protocol rule).
- Coinbase outputs cannot be spent for 100 blocks.
- Handle reorgs: keep txid-to-block mapping and re-evaluate when `getblockhash(height)` changes.
- `bitcoin-cli getrawtransaction <txid> true` shows `confirmations`.

## Verify
- [ ] Your accounting credits deposits only after your chosen depth and un-credits on reorg.
