---
id: computing-software.blockchain-and-web3.ethereum-evm.transaction-types-and-receipts
name: transaction-types-and-receipts
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [transaction-types, tx-receipt, transaction-status]
level: practitioner
status: draft
description: "Read a transaction receipt: status, gasUsed, logs, contractAddress, and the legacy, access-list and EIP-1559 transaction types."
sources:
  - https://ethereum.org/en/developers/docs/transactions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Types and receipts
- Types: 0 legacy, 1 access list (EIP-2930), 2 dynamic fee (EIP-1559). Newer types exist (blob transactions, type 3); check client docs for current ones.
- `eth_getTransactionReceipt(hash)` gives `status` (1 success, 0 reverted), `gasUsed`, `effectiveGasPrice`, `logs`, `contractAddress` (for creations).
- A reverted tx is still mined and still costs gas.
- `cast receipt <hash>` and `cast tx <hash>` decode these quickly; `cast run <hash>` replays a transaction against a fork.
- Gotcha: a `null` receipt means not yet mined, not failed.

## Verify
- [ ] You can state why a tx failed from `status`, revert data and gas used vs gas limit.
