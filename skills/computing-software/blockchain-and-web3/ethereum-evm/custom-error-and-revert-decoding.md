---
id: computing-software.blockchain-and-web3.ethereum-evm.custom-error-and-revert-decoding
name: custom-error-and-revert-decoding
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [revert-data-decoding, error-selector, panic-codes]
level: practitioner
status: draft
description: "Decode revert reasons: Error(string), Panic(uint256) codes and custom error selectors."
sources:
  - https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decoding reverts
- `Error(string)` selector `0x08c379a0`; `Panic(uint256)` selector `0x4e487b71`; custom errors use the first 4 bytes of their signature hash.
- Common panic codes: 0x01 assert, 0x11 arithmetic overflow, 0x12 division by zero, 0x21 bad enum, 0x31 pop on empty array, 0x32 index out of bounds, 0x41 out of memory.
- `cast 4byte 0x<selector>` looks up candidate signatures; with the ABI use `cast abi-decode`, or in Foundry tests `vm.expectRevert(Err.selector)`.
- Gotcha: empty revert data (`0x`) means `revert()` with no reason, or out-of-gas in a subcall.

## Verify
- [ ] The decoded selector matches an error defined in the ABI.
