---
id: computing-software.blockchain-and-web3.smart-contract-security.reentrancy-pattern-and-fix
name: reentrancy-pattern-and-fix
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [reentrancy-fix, swc-107, cei-pattern, bc-sec-reentrancy]
level: practitioner
status: draft
description: "Spot single-function reentrancy (external call before state update) and fix with checks-effects-interactions and a guard."
sources:
  - https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/
  - https://swcregistry.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reentrancy: pattern and fix
Pattern: a function makes an external call (ETH send, token hook) before updating its own accounting, so the callee can call back while state is stale.
Review checklist:
- List every external call (`call`, token transfers, ERC-721/1155 receiver hooks, ERC-777 hooks).
- For each, check that every state variable relied on after or by a re-entered call is already updated.
Fix:
1. Checks-effects-interactions: update balances, then call out.
2. `nonReentrant` on all entry points that share the state.
3. Pull payments: record owed amounts and let users withdraw.
Gotcha: ERC-777 and ERC-721/1155 receiver hooks create reentrancy through token transfers that look harmless.

## Verify
- [ ] A test with a malicious receiver contract that re-enters fails and leaves balances correct.
