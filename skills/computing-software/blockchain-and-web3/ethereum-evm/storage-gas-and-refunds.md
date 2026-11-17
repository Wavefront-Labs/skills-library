---
id: computing-software.blockchain-and-web3.ethereum-evm.storage-gas-and-refunds
name: storage-gas-and-refunds
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [sstore-cost, gas-refunds, warm-cold-access]
level: advanced
status: draft
description: "Understand cold versus warm access, SSTORE costs and refund caps so gas profiling makes sense."
sources:
  - https://www.evm.codes/
  - https://eips.ethereum.org/EIPS/eip-2929
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage gas
- EIP-2929: the first access to an address or slot in a tx is cold (more expensive, e.g. 2100 for SLOAD), later accesses are warm (100). Verify numbers on evm.codes for your fork.
- SSTORE cost depends on original, current and new value (EIP-2200/3529). Zero to non-zero is the most expensive; non-zero to non-zero is cheaper.
- Refunds (EIP-3529) are capped at one fifth of gas used and no longer support gas-token tricks.
- Practical: cache storage reads in memory, write once at the end.

## Verify
- [ ] `forge test --gas-report` shows the reduction after caching slots.
