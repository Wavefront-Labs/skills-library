---
id: computing-software.blockchain-and-web3.solidity.namespaced-storage-erc7201
name: namespaced-storage-erc7201
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [erc7201-namespaced, storage-struct-slot, custom-storage-location]
level: sme
status: docs-checked
description: "Use ERC-7201 namespaced storage for upgrade-safe layouts."
sources:
  - https://eips.ethereum.org/EIPS/eip-7201
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ERC-7201
- Group state into a struct stored at a namespaced slot: `erc7201(id) = keccak256(keccak256(id) - 1) & ~0xff`. In Solidity: `keccak256(abi.encode(uint256(keccak256(bytes(id))) - 1)) & ~bytes32(uint256(0xff))`.
- Annotate the struct with `@custom:storage-location erc7201:<NAMESPACE_ID>` so tools can validate it.
- ERC-7201 motivates this for upgradeable contracts, where adding state variables in an upgrade is hard because of storage layout.

## Verify
- [ ] The documented constant matches the formula output and tooling accepts the annotation.

## Checked

2026-11-02. Confirmed against EIP-7201 (formula, annotation, upgradeable motivation, example constant for example.main). Removed as not on the page: the assembly slot-assignment snippet, "layout at" custom base slot, OpenZeppelin v5 usage and "no storage gaps needed", cast keccak.
Method: documentation only; no commands were run.
