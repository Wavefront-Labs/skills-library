---
id: computing-software.blockchain-and-web3.consensus-and-protocols.finality-types-and-tradeoffs
name: finality-types-and-tradeoffs
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [probabilistic-finality, economic-finality, finality-gadget]
level: practitioner
status: draft
description: "Compare finality models and what they mean for exchange deposits, bridges and rollups."
sources:
  - https://ethereum.org/en/developers/docs/consensus-mechanisms/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finality types
- Probabilistic (PoW): reversal chance falls with depth.
- Deterministic/BFT: once committed, final.
- Economic (Ethereum FFG): reversing a finalized checkpoint would require burning at least 1/3 of total stake via slashing.
- Applications choose block tags accordingly: Ethereum `safe` and `finalized`; bridges and rollups should wait for finality before releasing funds.
- L2 "soft" confirmations from a sequencer are not L1 finality.

## Verify
- [ ] Your integration documents which finality level each operation waits for.
