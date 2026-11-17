---
id: computing-software.blockchain-and-web3.solidity.value-types-and-casting
name: value-types-and-casting
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-value-types, integer-downcast, address-payable, bc-sol-types]
level: intro
status: docs-checked
description: "Choose uint/int/address/bytesN/bool/enum types and cast between them without silent truncation."
sources:
  - https://docs.soliditylang.org/en/latest/types.html
  - https://docs.soliditylang.org/en/latest/control-structures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Value types and casting
- Integers `uint8`..`uint256` and `int8`..`int256` in steps of 8 (`uint`/`int` alias `uint256`/`int256`); `address` and `address payable`; `bytes1`..`bytes32`; `bool`; enums; user-defined value types (`type Price is uint128;`).
- Explicit integer downcasts of runtime values cut off the higher-order bits without any check: `uint32 a = 0x12345678; uint16(a)` is `0x5678`. Check the range yourself before casting down.
- Since 0.8.0, explicit conversion of a literal is as strict as implicit conversion: the literal must fit the target type, so `uint8(300)` does not compile.
- `int` to `uint` of the same size reinterprets the two's complement bits: `uint(-3)` is `0xfff...fd`.
- Explicit conversions to `address` are allowed only from `bytes20` and `uint160`; a larger type such as `bytes32` converted to `address` is truncated.
- `address payable` has the extra members `transfer` and `send`; convert with `payable(a)`. A contract type converts to or from `address payable` only if it has a receive or payable fallback function.
- Fixed bytes pad and cut on the right (`bytes2` to `bytes4` pads at the end), integers on the left. Explicit conversions between integers and fixed bytes are allowed only at the same size; for other sizes chain conversions, for example `uint32(bytes4(a))`.
- `bytes` arrays and calldata slices convert explicitly to `bytesN`: truncated at the end if longer, zero-padded at the end if shorter. `bytes(s)` converts a `string` to `bytes`.
- Converting an integer to an enum checks the range at runtime and reverts with Panic 0x21 if the value is too big or negative. Enums need at least one member, default to the first, and have at most 256 members.

## Verify
- [ ] A unit test that downcasts a value above the target max shows the truncated result (or the guard reverts), and an out-of-range enum conversion reverts.

## Checked

Confirmed against Solidity docs types/value_types.rst, types/conversion.rst, types/reference_types.rst (bytes(s)) and control-structures.rst (Panic 0x21). Removed: the draft's `uint8(300)` is 44 example (it is a compile error since 0.8.0) and the OpenZeppelin SafeCast recommendation (OZ docs not read).

Method: docs-checked 2026-11-09 against Solidity docs types (value types, conversion, reference types) and control structures (raw rst on GitHub).
