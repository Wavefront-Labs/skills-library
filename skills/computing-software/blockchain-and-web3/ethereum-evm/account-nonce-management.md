---
id: computing-software.blockchain-and-web3.ethereum-evm.account-nonce-management
name: account-nonce-management
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [account-nonce, stuck-transaction, replace-transaction]
level: practitioner
status: draft
description: "Reason about account nonces, diagnose a stuck pending transaction and replace it by reusing the nonce with a higher fee."
sources:
  - https://ethereum.org/en/developers/docs/transactions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nonce handling
- A transaction's `nonce` must equal the sender's current transaction count; nonces are strictly sequential, so one stuck low-fee transaction blocks all later ones.
- Read both: `eth_getTransactionCount(addr, "latest")` (mined) vs `"pending"` (mempool). A gap means pending transactions exist.
- Replace a stuck tx: send a new tx with the same nonce and a fee bump. Nodes require a minimum bump to replace (client policy; Geth's default is 10%, check yours).
- Cancel: send a 0-value tx to yourself with the same nonce and higher fees.
- Gotcha: bots sending from one key concurrently must allocate nonces locally, not re-read from the node each time.

## Verify
- [ ] After replacement, `latest` and `pending` counts converge.
