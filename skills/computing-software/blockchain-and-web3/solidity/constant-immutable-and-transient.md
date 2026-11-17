---
id: computing-software.blockchain-and-web3.solidity.constant-immutable-and-transient
name: constant-immutable-and-transient
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [constant-immutable, transient-storage, eip1153]
level: practitioner
status: docs-checked
description: "Choose constant, immutable or transient variables to avoid storage reads and understand their limits."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#constant-and-immutable-state-variables
  - https://eips.ethereum.org/EIPS/eip-1153
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# constant, immutable, transient
- `constant`: the compiler replaces each occurrence with its value and does not reserve a storage slot.
- `immutable`: the value can be assigned at construction time and is then fixed; it is stored in the contract code and conflicts with transient storage.
- Transient storage (EIP-1153, opcodes `TLOAD` `0x5c` and `TSTORE` `0x5d`): behaves like storage but is discarded after every transaction; the EIP lists reentrancy locks as a use case.
- The Solidity docs have a "Transient Storage" section for the `transient` keyword; check your compiler version for support.
- A transient lock is cleared per transaction, not per call; design accordingly.

## Verify
- [ ] Gas report drops for functions reading the former storage variable.
## Checked
2026-11-02. Confirmed against Solidity docs "Contracts" (constant and immutable, Transient Storage sections) and EIP-1153. Removed: upgradeable-proxy advice, flash accounting, the inline-assembly fallback and the no-SLOAD gas claim.
Method: documentation only; no commands were run.
