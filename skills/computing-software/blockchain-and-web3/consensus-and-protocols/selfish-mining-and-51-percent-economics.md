---
id: computing-software.blockchain-and-web3.consensus-and-protocols.selfish-mining-and-51-percent-economics
name: selfish-mining-and-51-percent-economics
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [selfish-mining, majority-attack-economics, confirmation-security]
level: advanced
status: draft
description: "Understand the economic limits behind confirmation depth and what majority attacks can and cannot do."
sources:
  - https://bitcoin.org/bitcoin.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attack models (conceptual)
- With majority hash power an attacker can double-spend their own recent transactions and censor; they cannot steal others' coins or change rules enforced by full nodes.
- Selfish mining research shows pools below 50% can gain unfair revenue by withholding blocks; practical impact depends on network propagation.
- Smaller PoW chains with rentable hash power are cheaper to attack; confirmation counts for exchanges are scaled accordingly.
- Defensive takeaways: require more confirmations on low-hash chains, monitor for deep reorgs, and run your own validating node.

## Verify
- [ ] Your deposit policy states confirmation counts per chain with a rationale.
