---
id: computing-software.blockchain-and-web3.consensus-and-protocols.proof-of-work-and-difficulty
name: proof-of-work-and-difficulty
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [proof-of-work, difficulty-adjustment, nakamoto-consensus, bc-con-pow]
level: intro
status: draft
description: "Explain hashing, target, the 2016-block difficulty retarget and the longest-chain rule."
sources:
  - https://bitcoin.org/bitcoin.pdf
  - https://developer.bitcoin.org/devguide/mining.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proof of work
- Miners hash block headers (double SHA-256) with varying nonce until the hash is below the target.
- Difficulty adjusts every 2016 blocks aiming at about 10 minutes per block (target timespan two weeks).
- Fork choice: follow the chain with the most accumulated work ("heaviest", loosely longest).
- Security assumption: honest majority of hash power; a majority attacker can reorder recent history but not forge signatures.
- Observe: `bitcoin-cli getblockchaininfo` (difficulty), `getmininginfo`, `getchaintips`.

## Verify
- [ ] You can compute the expected retarget given actual timespan, clamped to a factor of 4.
