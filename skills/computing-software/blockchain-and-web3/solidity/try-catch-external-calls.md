---
id: computing-software.blockchain-and-web3.solidity.try-catch-external-calls
name: try-catch-external-calls
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [try-catch-solidity, low-level-call-result, returndata-bomb]
level: advanced
status: docs-checked
description: "Handle failing external calls with try/catch or low-level call results, including what try/catch does not catch."
sources:
  - https://docs.soliditylang.org/en/latest/control-structures.html#try-catch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try/catch
```solidity
try token.balanceOf(user) returns (uint256 b) { ... }
catch Error(string memory reason) { ... }
catch (bytes memory data) { ... }
```
- `try` must be followed by an external function call or a contract creation (`new C()`). Errors inside the rest of the expression (for example internal calls) are not caught, only a revert in the external call itself.
- An error while decoding the return data is not caught by the catch clauses; it reverts the current contract. A decoding error inside `catch Error(string memory)` is caught by a low-level catch clause if one exists.
- Clauses: `catch Error(string memory reason)` for `revert("...")` or `require(false, "...")`; `catch Panic(uint code)` for assert failures, division by zero, bad array access and overflow; `catch (bytes memory data)` for anything else, including no error data; `catch { }` when you do not need the data. To catch every case you need a bare `catch` or the `bytes memory` clause.
- When a catch block runs, the external call's state changes have been reverted. The failure may come deeper in the call chain or from running out of gas, so do not assume the message is the callee's own; the caller always keeps at least 1/64th of the gas.
- Low-level `call`, `delegatecall` and `staticcall` do not bubble up exceptions: they return `(bool success, bytes memory data)`, and `success` is also `true` when the target account does not exist. Never ignore the bool result, and check the target has code first if that matters.

## Verify
- [ ] A test with a callee that reverts exercises the catch branch.

## Checked

Confirmed against Solidity docs control-structures.rst (try/catch rules and notes, 1/64th gas retention, low-level call behaviour including non-existent account returning true) and types/value-types.rst (call, delegatecall, staticcall return a bool and bytes memory). Removed the return-data-bomb gas claim and its assembly cap recipe because no page read describes it.

Method: docs-checked 2026-11-09 against Solidity docs control-structures.rst and types/value-types.rst (raw rst on GitHub).
