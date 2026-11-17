---
id: computing-software.blockchain-and-web3.smart-contract-security.eip712-typed-data-implementation
name: eip712-typed-data-implementation
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [eip712-domain, typed-data-hash, struct-hash]
level: advanced
status: docs-checked
description: "Build the EIP-712 domain separator and struct hash correctly in a contract and match wallet signing output."
sources:
  - https://eips.ethereum.org/EIPS/eip-712
  - https://docs.openzeppelin.com/contracts/5.x/api/utils#EIP712
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EIP-712
- The signed digest is built from a domain separator and the hash of the struct (`hashStruct`); the EIP defines `typeHash`, `encodeData` and `domainSeparator`.
- Domain fields include `name`, `version`, `chainId` and `verifyingContract` (and an optional `salt`).
- The type string is hashed, so spacing and member order matter; mismatches usually come from a wrong type string.
- OpenZeppelin provides an `EIP712` utility contract (5.x utils API).

## Verify
- [ ] A test signature your contract accepts, and a changed field is rejected.

## Checked

2026-11-02. Confirmed against EIP-712 (typeHash, encodeData, domainSeparator, domain field names) and the OpenZeppelin 5.x utils page (EIP712 contract). Removed as not verified verbatim: the explicit digest and hashStruct formulas with \x19\x01, the member-encoding rules, the _hashTypedDataV4 helper name, cast wallet sign --data, vm.sign.
Method: documentation only; no commands were run.
