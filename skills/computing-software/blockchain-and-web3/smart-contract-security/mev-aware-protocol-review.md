---
id: computing-software.blockchain-and-web3.smart-contract-security.mev-aware-protocol-review
name: mev-aware-protocol-review
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [mev-review, sandwich-attack-defence, liquidation-incentives]
level: advanced
status: draft
description: "Review protocol functions for value that arbitrage, liquidation and sandwich searchers can extract, and decide what is acceptable."
sources:
  - https://ethereum.org/en/developers/docs/mev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MEV review
- For each permissionless function ask: can ordering around it extract value, and from whom (users, protocol)?
- Liquidations: bonuses must be big enough to attract keepers but not so large they harm borrowers.
- Rebases/oracle updates: predictable updates can be front-run; use gradual updates or fees.
- Keep a document listing accepted MEV and the mitigations for the rest.

## Verify
- [ ] Each permissionless function has a written note on ordering sensitivity.
