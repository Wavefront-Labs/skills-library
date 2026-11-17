---
id: computing-software.blockchain-and-web3.consensus-and-protocols.soft-vs-hard-forks
name: soft-vs-hard-forks
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [soft-fork, hard-fork, chain-split, bc-con-forks]
level: practitioner
status: draft
description: "Differentiate rule tightening (soft fork) from loosening (hard fork) and what node operators must do."
sources:
  - https://ethereum.org/en/history/
  - https://developer.bitcoin.org/devguide/block_chain.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft and hard forks
- Soft fork: new rules are a subset of old rules; old nodes still accept new blocks (for example segwit, taproot on Bitcoin).
- Hard fork: rules loosen or change incompatibly; non-upgraded nodes reject new blocks and follow a different chain unless everyone upgrades (Ethereum network upgrades are coordinated hard forks).
- Operators: track client release notes, upgrade before the activation epoch/block, and watch for chain splits afterwards.
- Applications: replay protection (chain IDs) matters after contentious splits.

## Verify
- [ ] Your client version meets the minimum for the next scheduled upgrade, per the client's release notes.
