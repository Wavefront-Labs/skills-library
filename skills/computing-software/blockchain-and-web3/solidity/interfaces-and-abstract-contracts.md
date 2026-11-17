---
id: computing-software.blockchain-and-web3.solidity.interfaces-and-abstract-contracts
name: interfaces-and-abstract-contracts
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-interfaces, abstract-contract, interface-id]
level: practitioner
status: docs-checked
description: "Define interfaces and abstract contracts, and compute ERC-165 interface IDs."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#interfaces
  - https://eips.ethereum.org/EIPS/eip-165
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interfaces and abstracts
- Interface: no implemented functions, no constructor, no state variables, no modifiers; all functions are external and implicitly virtual. It may inherit only from other interfaces. It can declare enums, structs, events and errors, reachable as `Token.TokenType`.
- Abstract contract: must be marked `abstract` when any function is unimplemented or a base constructor lacks arguments (it may be marked abstract anyway). It cannot be instantiated directly; a child that does not implement everything must be abstract too. Unimplemented functions outside interfaces need `virtual`.
- ERC-165: an interface identifier is the XOR of all its function selectors, for example `type(I).interfaceId`. A compliant contract implements `supportsInterface(bytes4) external view returns (bool)` using at most 30,000 gas. It returns true for `0x01ffc9a7` (ERC-165 itself) and for each interface it implements, and false for `0xffffffff` and anything else.
- Code against interfaces to call other contracts: `IERC20(token).balanceOf(user)`.
- High-level calls through an interface check that the target has code, except when return data is decoded afterwards (since 0.8.10); low-level calls on addresses do not check.

## Verify
- [ ] `supportsInterface(type(I).interfaceId)` returns true for each advertised interface, and `supportsInterface(0xffffffff)` returns false.

## Checked

Confirmed against Solidity docs contracts/interfaces.rst, contracts/abstract-contracts.rst and contracts/inheritance.rst, control-structures.rst (extcodesize check and the 0.8.10 note), and the ERC-165 text (raw ercs repository; the eips.ethereum.org URL points at the same standard): interface restrictions, XOR identifier, 0x01ffc9a7, 0xffffffff, 30,000 gas. Rewrote the abstract-contract rule (marking is required, not merely "at least one unimplemented function") and the extcodesize gotcha, which was imprecise.

Method: docs-checked 2026-11-09 against Solidity docs interfaces, abstract-contracts, control-structures, units-and-global-variables (type(I).interfaceId) (raw rst) and ERC-165 (ethereum/ercs erc-165.md).
