---
id: computing-software.blockchain-and-web3.ethereum-evm.indexing-and-subgraph-basics
name: indexing-and-subgraph-basics
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [subgraph-indexing, the-graph, event-driven-indexer]
level: practitioner
status: draft
description: "Choose between direct RPC reads, a subgraph or a custom indexer for contract data."
sources:
  - https://thegraph.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing choices
- Few reads: call the contract directly (`eth_call`), cache by block.
- History or aggregates: index events. The Graph subgraphs define a schema, a manifest of data sources and event handlers (AssemblyScript) and expose a GraphQL API; custom indexers (ethers/viem + Postgres) give full control.
- Emit events designed for indexing (see event design) and include ids.
- Handle reorgs (subgraphs do this for you; custom code must).
- Pin start blocks to deployment blocks to keep sync fast.

## Verify
- [ ] Indexed totals match on-chain view functions at the same block.
