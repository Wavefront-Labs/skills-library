---
id: computing-software.blockchain-and-web3.consensus-and-protocols.finality-and-slashing
name: finality-and-slashing
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [casper-ffg-finality, slashing-conditions, inactivity-leak]
level: advanced
status: draft
description: "Explain justified and finalized checkpoints, slashing conditions and the inactivity leak."
sources:
  - https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/
  - https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/rewards-and-penalties/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finality and slashing
- Casper FFG: a checkpoint (first slot of an epoch) is justified with 2/3 of stake attesting; finalized when the next checkpoint is also justified. Finalization normally takes about two epochs (about 13 minutes).
- Slashing offences: double proposal, and attestation violations (double vote, surround vote). Penalties include forced exit and an immediate penalty plus a correlated penalty scaled by how many validators were slashed around the same time.
- Inactivity leak: if finality stalls, non-participating validators lose stake gradually until 2/3 participation returns.
- Operators avoid slashing by never running the same keys on two machines and using slashing-protection databases when migrating.

## Verify
- [ ] Your validator migration runbook includes exporting and importing slashing-protection data.
