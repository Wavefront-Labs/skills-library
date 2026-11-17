---
id: computing-software.blockchain-and-web3.consensus-and-protocols.ethereum-pos-validators-and-attestations
name: ethereum-pos-validators-and-attestations
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [ethereum-pos, slots-and-epochs, attestations, bc-con-pos]
level: intro
status: draft
description: "Describe slots (12 s), epochs (32 slots), proposers, committees and attestations."
sources:
  - https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ethereum proof of stake
- A slot is 12 seconds; an epoch is 32 slots. One validator proposes a block per slot; others attest.
- Validators stake ETH (32 ETH per validator originally; later upgrades allow higher effective balances, verify current rules).
- Attestations vote on the head of the chain and on checkpoints (source and target).
- Execution clients (e.g. Geth, Nethermind) and consensus clients (e.g. Lighthouse, Prysm) run side by side, linked by the Engine API.
- Rewards come from attestations, proposals and sync committees; penalties for being offline.

## Verify
- [ ] Beacon explorer data for a slot shows proposer index and attestation inclusion.
