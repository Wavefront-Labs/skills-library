---
id: computing-software.blockchain-and-web3.solidity.require-revert-assert-custom-errors
name: require-revert-assert-custom-errors
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [custom-errors, require-vs-assert, revert-with-error, bc-sol-errors]
level: practitioner
status: docs-checked
description: "Use custom errors for cheaper, typed reverts and reserve assert for invariants."
sources:
  - https://docs.soliditylang.org/en/latest/control-structures.html#error-handling-assert-require-revert-and-exceptions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Errors
```solidity
error InsufficientBalance(uint256 have, uint256 need);
if (bal < amt) revert InsufficientBalance(bal, amt);
```
- A custom error is identified by a 4-byte selector, so it is usually much cheaper than a revert string, and it carries typed arguments. The `revert CustomError(args)` statement is the main form.
- `require(cond, CustomError())` exists from 0.8.26 in the via-ir pipeline only, and from 0.8.27 in the legacy pipeline; custom errors themselves arrived in 0.8.4; check your compiler version. `require` arguments are evaluated even when the condition holds, so keep them free of side effects.
- `require(bool)` reverts with no data at all; `require(bool, string)` reverts with `Error(string)`.
- `require` for input and external conditions; `assert` for conditions that must never be false. A failing `assert` raises `Panic(uint256)` with code 0x01 and indicates a bug. Overflow is 0x11, division by zero 0x12, out-of-bounds index 0x32.
- A revert undoes all state changes of the current call and its sub-calls; a caller can catch it with try/catch, but the callee's changes stay reverted.

## Verify
- [ ] A test asserts the revert data equals the ABI-encoded selector and arguments of the expected custom error.

## Checked

Confirmed against Solidity docs control-structures.rst (assert, require, revert, Panic codes, custom errors cheaper because encoded in four bytes, revert semantics) and the compiler Changelog (custom errors: error keyword and revert statement listed under 0.8.4; 0.8.26: require(bool, Error) overload, via-ir only; 0.8.27: available in the legacy pipeline). Removed the Foundry vm.expectRevert snippet (Foundry book not readable).

Method: docs-checked 2026-11-09 against Solidity docs control-structures.rst and Changelog.md (raw on GitHub).
