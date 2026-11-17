---
id: computing-software.blockchain-and-web3.consensus-and-protocols.bft-consensus-fundamentals
name: bft-consensus-fundamentals
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [bft-consensus, byzantine-fault-tolerance, two-thirds-quorum, bc-con-bft]
level: advanced
status: draft
description: "Explain the 3f+1 requirement, quorum intersection, safety versus liveness and partial synchrony."
sources:
  - https://docs.cometbft.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BFT basics
- To tolerate f Byzantine nodes you need n >= 3f + 1; decisions need quorums of 2f + 1 so that any two quorums overlap in at least one honest node.
- Safety: no two honest nodes decide different values. Liveness: the system eventually decides. FLP shows both cannot be guaranteed in a fully asynchronous network; protocols assume partial synchrony (safety always, liveness after the network stabilises).
- Tendermint/CometBFT: rounds of propose, prevote, precommit; instant finality (no reorgs) but halts if more than 1/3 of voting power is offline.
- Compare with probabilistic finality in Nakamoto consensus.

## Verify
- [ ] For a validator set of 10 equal weights, you can state f, and the quorum size needed.
