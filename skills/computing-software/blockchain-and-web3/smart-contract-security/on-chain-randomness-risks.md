---
id: computing-software.blockchain-and-web3.smart-contract-security.on-chain-randomness-risks
name: on-chain-randomness-risks
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [weak-randomness, swc-120, verifiable-randomness, bc-sec-randomness]
level: practitioner
status: draft
description: "Avoid blockhash/timestamp randomness; use verifiable randomness or commit-reveal."
sources:
  - https://swcregistry.io/
  - https://docs.chain.link/vrf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Randomness
- `block.timestamp`, `blockhash`, `prevrandao` and similar are predictable or influenceable by proposers/validators and by contract callers in the same transaction.
- For value-bearing randomness use a verifiable randomness service (e.g. Chainlink VRF) with request/fulfil flow, or a commit-reveal with penalties.
- VRF fulfil callbacks must not revert and should be gas-bounded; handle the pending state for users.
- Do not let callers read results and revert if unfavourable: structure so the outcome is final at request time.

## Verify
- [ ] Test shows a caller cannot revert-and-retry to fish for outcomes.
