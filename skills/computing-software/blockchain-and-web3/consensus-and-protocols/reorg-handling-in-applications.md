---
id: computing-software.blockchain-and-web3.consensus-and-protocols.reorg-handling-in-applications
name: reorg-handling-in-applications
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [reorg-handling, finalized-block-tag, event-rollback]
level: practitioner
status: draft
description: "Design backends that tolerate chain reorganisations: confirmation depth, rollback and idempotency."
sources:
  - https://ethereum.org/en/developers/docs/apis/json-rpc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reorg handling
- Store block hash with every derived record; on each new head compare the parent hash with your stored chain and roll back to the common ancestor when it differs.
- Delay irreversible actions (credits, shipments) until the `finalized` tag (Ethereum) or N confirmations (Bitcoin).
- Make handlers idempotent and keyed by (blockHash, logIndex).
- Test by simulating a reorg with anvil snapshots (`evm_snapshot`/`evm_revert`) or Bitcoin regtest `invalidateblock`.

## Verify
- [ ] After a simulated 3-block reorg, database state equals a fresh index of the new chain.
