---
id: computing-software.blockchain-and-web3.solidity.libraries-and-using-for
name: libraries-and-using-for
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-libraries, using-for, delegatecall-library]
level: practitioner
status: docs-checked
description: "Write internal and external libraries and attach them with using-for; know the DELEGATECALL implication."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#libraries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Libraries
- Internal library functions (and everything they call) are included in the calling contract at compile time and reached with a plain `JUMP`; memory types are passed by reference.
- Public and external library functions are deployed once and called with `DELEGATECALL`, so `this`, `msg.sender`, `msg.value` and storage are the caller's. This is a real external call: memory and value arguments are copied; only storage references and internal calls avoid the copy.
- The compiled bytecode of a contract that uses a deployed library contains placeholders of the form `__$<34 hex chars>$__`. That bytecode is incomplete and must not be deployed until the placeholders are replaced by the library address, at compile time or with the linker.
- A library cannot have state variables, inherit or be inherited, receive Ether or be destroyed. Calling a non-view, non-pure library function with a plain `CALL` reverts (call protection).
- `using L for T;` attaches all non-private functions of library `L` to type `T` as members (the first parameter is the object). `using {f, g} for T;` attaches listed library or free functions, and `T` must convert implicitly to each first parameter. `using {f as +} for T global;` defines an operator on a user-defined value type, with a `pure` free function. `using` is active only in its own contract or file; `global` (file level, type defined in the same file) makes it apply wherever the type is visible.
- The idiom for a library function that works on storage is a `Data storage self` first parameter.

## Verify
- [ ] The deployed bytecode contains no unlinked placeholder (`__$...$__`).

## Checked

Confirmed against Solidity docs contracts/libraries.rst and contracts/using-for.rst: DELEGATECALL vs internal inlining, copy semantics, link placeholder format, library restrictions, call protection, and the using-for forms including `global` and operators. Removed the Foundry `forge create --libraries` and `foundry.toml` lines (Foundry book not readable) and the SafeMath example.

Method: docs-checked 2026-11-09 against Solidity docs contracts/libraries.rst and contracts/using-for.rst (raw rst on GitHub).
