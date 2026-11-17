---
id: computing-software.blockchain-and-web3.smart-contract-security.cross-function-and-readonly-reentrancy
name: cross-function-and-readonly-reentrancy
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [cross-function-reentrancy, read-only-reentrancy, view-reentrancy]
level: advanced
status: draft
description: "Detect reentrancy across functions or contracts, including view functions read mid-update, and apply defences."
sources:
  - https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-function and read-only reentrancy
- Cross-function: function A sends ETH before updating shared state; re-entry into function B, which uses that state, sees stale data. A guard on A alone is not enough: guard all functions sharing the state, or fix the ordering.
- Read-only: contract X's `view` price/ratio is read by protocol Y while X is mid-execution (after an external call, before state update). Y trusts a transient wrong value.
- Defences: make state consistent before any external call; expose a `nonReentrantView` check (revert in views if the lock is held); consumers of third-party views should check the provider's lock where available.
- Review rule: any `view` function used for pricing by other contracts is part of your security surface.

## Verify
- [ ] Test calls the view from inside a callback and expects a revert or a consistent value.
