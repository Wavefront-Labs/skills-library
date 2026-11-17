---
id: computing-software.blockchain-and-web3.solidity.storage-slot-layout-and-packing
name: storage-slot-layout-and-packing
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [storage-layout, variable-packing, forge-inspect-layout, bc-sol-storage]
level: advanced
status: docs-checked
description: "Predict slot assignment, pack variables into 32-byte slots and request the compiler's storage layout JSON."
sources:
  - https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slot layout
- State variables are assigned slots in declaration order starting at slot 0. Contiguous items needing under 32 bytes are packed into one slot if they fit: the first item is lower-order aligned and each value type uses only the bytes it needs.
- A value that does not fit the rest of a slot goes to the next one. Struct and array data always start a new slot, and items following them start a new slot too.
- With inheritance, order follows the C3-linearized order starting from the most base-ward contract, and variables of different contracts can share a slot.
- Mappings and dynamic arrays take one whole slot each (to base their hashed locations on); constant, immutable and transient variables do not occupy storage slots. A contract can set a custom base slot with `layout at <n>` (the layout shifts for the whole inheritance tree).
- Order small types together: `uint128, uint128, uint256` takes two slots, `uint128, uint256, uint128` takes three.
- Packing helps when the packed values are read or written together; writing one value of a shared slot requires reading the slot first, and types smaller than 32 bytes can cost more gas elsewhere. Memory values and function arguments are not packed.
- Request the layout from the compiler through the standard JSON interface; each storage entry has `astId`, `contract`, `label`, `offset` (bytes within the slot), `slot` (a string) and `type`, with type info in `types` (`encoding`, `label`, `numberOfBytes`). The format is documented as experimental.
- The layout rules count as part of Solidity's external interface (storage pointers can be passed to libraries), so they only change in breaking releases.

## Verify
- [ ] The layout output shows the intended slot and offset pairs.

## Checked

Confirmed against Solidity docs internals/layout_in_storage.rst (read in full): packing rules, inheritance order, custom layout, gas warning, JSON output fields. Removed the Foundry `forge inspect` command, the Hardhat `storageLayout` setting and `cast storage` (not readable or not on the page); the tag `forge-inspect-layout` is kept as a tag only.

Method: docs-checked 2026-11-09 against Solidity docs internals/layout_in_storage.rst (raw rst on GitHub).
