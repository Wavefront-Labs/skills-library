---
id: computing-software.blockchain-and-web3.solidity.inheritance-and-linearization
name: inheritance-and-linearization
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-inheritance, c3-linearization, super-call, bc-sol-inheritance]
level: practitioner
status: docs-checked
description: "Use multiple inheritance, override/virtual and understand the linearization order and constructor ordering."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#inheritance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance
- `contract C is A, B` lists direct bases from "most base-like" to "most derived" (the reverse of Python). Solidity uses C3 linearization; a graph with a contradictory order fails with "Linearization of inheritance graph impossible".
- `super.f()` calls `f` on the next contract in the final linearized order, not simply one of the direct bases; `Base.f()` names a specific base and can bypass others in a diamond.
- A function to be overridden needs `virtual`; the override needs `override`, and `virtual` again if it may be overridden further. When several unrelated bases define the same function, list them: `override(A, B)`. Since 0.8.8 `override` is not needed when overriding an interface function unless it is defined in multiple bases.
- Overriding may only change visibility from `external` to `public`, and may tighten mutability (`nonpayable` to `view` or `pure`, `view` to `pure`); `payable` cannot change. Private functions cannot be virtual.
- Base constructor arguments are given in the inheritance list (`is Base(7)`) or modifier-style in the derived constructor, not both. A contract that leaves some unset must be `abstract`.
- Constructors always run in linearized order from base to derived, regardless of the order of the arguments in the derived constructor.
- State variable shadowing is an error. Only a single contract is deployed; base code is compiled into it, and `super` calls are internal jumps.

## Verify
- [ ] The contract compiles without ambiguity errors; a test asserts the order in which `super` hooks run.

## Checked

Confirmed against Solidity docs contracts/inheritance.rst: C3 linearization and order, error text, super semantics, virtual/override rules, 0.8.8 interface override note, constructor argument rules, constructor order and state shadowing. Removed the Foundry `forge inspect storage-layout` tip (Foundry book not readable) and the "keep hierarchies shallow" opinion line.

Method: docs-checked 2026-11-09 against Solidity docs contracts/inheritance.rst (raw rst on GitHub).
