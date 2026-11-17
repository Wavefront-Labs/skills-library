---
id: computing-software.blockchain-and-web3.solidity.mappings-arrays-and-structs
name: mappings-arrays-and-structs
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-mappings, dynamic-array-storage, struct-packing-basics]
level: practitioner
status: docs-checked
description: "Pick mappings versus arrays, understand mapping non-iterability and delete semantics."
sources:
  - https://docs.soliditylang.org/en/latest/types.html#mapping-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mappings, arrays, structs
- Mapping: every possible key exists and maps to the type's default (all-zero) value. There is no length and no concept of a key set, and you cannot iterate over a mapping or enumerate its keys. Track membership yourself (for example a `bool` field in the value struct) if "never set" must differ from "zero".
- To enumerate, keep a parallel array of keys and build the iteration on top of the mapping; the docs show an iterable-mapping library built this way.
- `delete arr[i]` resets that element to its default and leaves the length unchanged, so it leaves a gap. To remove an element without a gap, move the last element into the slot and call `pop()`: `arr[i] = arr[arr.length-1]; arr.pop();`. `pop()` implicitly deletes the removed element, and its gas cost grows with the size of that element.
- `delete` on a struct resets every member but has no effect on mapping members (their keys are unknown); `delete m[k]` on a mapping deletes that single key's value.
- `push()` on a dynamic storage array appends a zero-initialised element at constant gas cost.
- Nested mapping: `mapping(address => mapping(address => uint256)) allowance;`.

## Verify
- [ ] Removal test: after swap-and-pop, the length decreased and the moved element's index is updated wherever you track it.

## Checked

Confirmed against Solidity docs types/mapping-types.rst (default values, no length or iteration, iterable-mapping example), types/operators.rst (delete semantics for arrays, structs and mappings) and types/reference-types.rst (push, pop and their gas notes). Removed: O(1) lookup wording, the OpenZeppelin EnumerableSet/EnumerableMap tip, and the unbounded-loop gas DoS line (not on pages read).

Method: docs-checked 2026-11-09 against Solidity docs types/mapping-types.rst, types/operators.rst and types/reference-types.rst (raw rst on GitHub).
