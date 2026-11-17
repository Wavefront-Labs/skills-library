---
id: computing-software.blockchain-and-web3.solidity.mapping-and-array-slot-computation
name: mapping-and-array-slot-computation
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [mapping-slot, keccak-slot, dynamic-array-slot]
level: advanced
status: docs-checked
description: "Compute where a mapping entry or dynamic array element lives in storage."
sources:
  - https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html#mappings-and-dynamic-arrays
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping and array slots
- A mapping or dynamic array occupies one 32-byte slot `p` in the normal layout; its contents live elsewhere, found with Keccak-256.
- `mapping(K => V)` at slot `p`: the value for key `k` is at `keccak256(h(k) . p)`, where `.` is concatenation. For value types `h` pads the key to 32 bytes; for strings and byte arrays `h(k)` is the unpadded data. The mapping's own slot stays empty. Nested mappings apply the rule repeatedly, and for a struct value you add the member's slot offset.
- Dynamic array at slot `p`: `p` holds the length; data starts at `keccak256(p)`, one element after the other, with elements of 16 bytes or less sharing slots. For `uint24[][] x` at `p`, element `x[i][j]` is in slot `keccak256(keccak256(p) + i) + floor(j / floor(256 / 24))`.
- `bytes` and `string`: if the data is at most 31 bytes, it is stored left-aligned in the slot and the lowest-order byte holds `length * 2`. If it is 32 bytes or more, slot `p` holds `length * 2 + 1` and the data is at `keccak256(p)`. The lowest bit tells you which form is in use.
- Worked example from the docs: with `uint x;` then `mapping(uint => mapping(uint => S)) data;` where `S` is `{uint16 a; uint16 b; uint256 c;}`, `data` is at slot 1 and `data[4][9].c` is at `keccak256(uint256(9) . keccak256(uint256(4) . uint256(1))) + 1`.
- Use this to debug and to check an upgrade's layout; storage is public regardless.

## Verify
- [ ] A storage read of the computed slot equals the public getter's return value.

## Checked

Confirmed against Solidity docs internals/layout_in_storage.rst (read in full): mapping and array formulas, key padding rule, bytes/string encodings, worked example. Removed the Foundry `cast index` and `cast storage` commands (Foundry book not readable).

Method: docs-checked 2026-11-09 against Solidity docs internals/layout_in_storage.rst (raw rst on GitHub).
