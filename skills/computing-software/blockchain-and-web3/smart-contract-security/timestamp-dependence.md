---
id: computing-software.blockchain-and-web3.smart-contract-security.timestamp-dependence
name: timestamp-dependence
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [timestamp-dependence, swc-116, time-window-safety]
level: intro
status: draft
description: "Use block.timestamp only for coarse windows and understand the drift tolerance."
sources:
  - https://swcregistry.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timestamp dependence
- Proposers can nudge `block.timestamp` slightly within consensus rules; treat it as accurate to about seconds, not exact.
- Safe uses: deadlines of hours/days, vesting schedules.
- Unsafe: sub-minute timing for fairness-critical logic, randomness.
- L2s may update timestamps differently; check the chain's docs.
- Use `block.number` only when the block time of the chain is known and stable (and it differs per chain).

## Verify
- [ ] Tests use `vm.warp` to cross boundaries exactly at, before and after thresholds.
