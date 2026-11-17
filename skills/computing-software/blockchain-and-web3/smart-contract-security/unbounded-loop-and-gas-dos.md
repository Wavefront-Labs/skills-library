---
id: computing-software.blockchain-and-web3.smart-contract-security.unbounded-loop-and-gas-dos
name: unbounded-loop-and-gas-dos
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [unbounded-loop, swc-128, block-gas-limit-dos, bc-sec-dos]
level: practitioner
status: draft
description: "Remove unbounded iteration and per-user loops that can exceed the block gas limit."
sources:
  - https://swcregistry.io/
  - https://consensys.github.io/smart-contract-best-practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gas DoS
- Looping over a user-growable array (payouts, holders) eventually exceeds the block gas limit and locks the function.
- Fix: pagination (`start`, `count`), pull payments, or accumulators (reward-per-share) that avoid iteration.
- Third-party-controlled recipients: a failing receiver can block a batch payout (SWC-113). Isolate each transfer or use pull payments.
- Cap array sizes in inputs.

## Verify
- [ ] Test inserts the maximum supported items and the worst-case function stays well below the block gas limit.
