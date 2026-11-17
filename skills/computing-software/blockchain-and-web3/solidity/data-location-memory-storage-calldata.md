---
id: computing-software.blockchain-and-web3.solidity.data-location-memory-storage-calldata
name: data-location-memory-storage-calldata
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-data-location, storage-pointer, calldata-vs-memory]
level: practitioner
status: docs-checked
description: "Use storage, memory and calldata correctly for arrays, structs and strings, and avoid stale-copy bugs."
sources:
  - https://docs.soliditylang.org/en/latest/types.html#data-location
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data locations
- `storage` reference = pointer to persistent state; `memory` = a copy; `calldata` = read-only external input, no copy.
- `Position storage p = positions[id]; p.amount = 0;` writes state. `Position memory p = positions[id]; p.amount = 0;` changes only the copy: a classic silent bug.
- An assignment or type conversion that changes the data location always incurs an automatic copy; assignments inside the same data location only copy in some cases for storage types.
- Dynamically-sized storage arrays support `.push()`/`.push(value)` to append an element.

## Verify
- [ ] Test asserts state changed after the function mutates a struct via storage pointer.
## Checked
2026-11-02. Confirmed against the Solidity docs "Types" (reference types and data location): copy-on-location-change rule, same-location assignment, and storage array `push`. Removed: calldata gas claim, "storage to storage by reference" rule and the memory-array resize claim (not confirmed on the page).
Method: documentation only; no commands were run.
