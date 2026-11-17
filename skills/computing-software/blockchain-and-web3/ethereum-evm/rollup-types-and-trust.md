---
id: computing-software.blockchain-and-web3.ethereum-evm.rollup-types-and-trust
name: rollup-types-and-trust
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [rollup-types, optimistic-rollup, zk-rollup, bc-eth-l2]
level: intro
status: draft
description: "Explain how optimistic and ZK rollups settle on Ethereum, their withdrawal delay and trust assumptions."
sources:
  - https://ethereum.org/en/developers/docs/scaling/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rollups
- Both execute off-chain and post data and state commitments to Ethereum L1.
- Optimistic: assume validity, allow a challenge window (commonly about 7 days) for fraud proofs; withdrawals to L1 wait that window unless a fast bridge fronts liquidity.
- ZK: post a validity proof; final on L1 once the proof verifies.
- Trust questions: who can upgrade the rollup contracts, is proving or challenging permissionless, who runs the sequencer, can users force-include via L1.
- Data availability on L1 (calldata or blobs) separates rollups from validiums.

## Verify
- [ ] For a chosen L2 you can name its proof system, sequencer model and upgrade admin (from its docs or an L2 risk dashboard).
