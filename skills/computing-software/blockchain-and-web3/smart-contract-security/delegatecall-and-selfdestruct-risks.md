---
id: computing-software.blockchain-and-web3.smart-contract-security.delegatecall-and-selfdestruct-risks
name: delegatecall-and-selfdestruct-risks
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [delegatecall-risks, swc-112, selfdestruct-deprecation]
level: advanced
status: draft
description: "Restrict delegatecall targets and understand SELFDESTRUCT changes."
sources:
  - https://swcregistry.io/
  - https://eips.ethereum.org/EIPS/eip-6780
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# delegatecall and selfdestruct
- `delegatecall` runs foreign code with your storage, `msg.sender` and balance. Never delegatecall to an address a user can influence. Library-like targets must be immutable or governance-controlled.
- Layout must match between caller and callee; mismatches corrupt state.
- A delegatecall target that selfdestructs (pre-Cancun) could destroy the caller; EIP-6780 limits SELFDESTRUCT to same-transaction creation only (post-Cancun), but do not rely on it for design.
- Multicall helpers that delegatecall to `address(this)` are fine, but preserve `msg.value` semantics carefully (double-spend of ETH in batched calls is a known pitfall).

## Verify
- [ ] No delegatecall destination is user-provided; layout tests pass.
