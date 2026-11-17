---
id: computing-software.blockchain-and-web3.ethereum-evm.function-selectors-and-calldata
name: function-selectors-and-calldata
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [function-selector, calldata-layout, abi-encode, bc-eth-abi]
level: practitioner
status: docs-checked
description: "Compute a 4-byte selector, hand-encode calldata with head/tail rules and decode unknown calldata."
sources:
  - https://docs.soliditylang.org/en/latest/abi-spec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selectors and calldata
- Selector = the first four bytes of the Keccak-256 hash of the function signature. The signature is the canonical form: no spaces and no parameter names.
- For computing the selector, `uint` and `int` must be written `uint256` and `int256`, and `address` is used for address types.
- Static types occupy 32-byte words in the head; for dynamic types the head holds an offset (in bytes, from the start of the value encoding) and the tail holds length and data.
- `abi.encodePacked` is a non-standard packed mode: shorter types are concatenated without padding, and the encoding is ambiguous with two or more dynamically-sized elements, so do not hash it for signatures.

## Verify
- [ ] Encoded calldata is accepted by `eth_call` and returns the expected value.
## Checked
2026-11-02. Confirmed against the Solidity "Contract ABI Specification": function selector, canonical types, head/tail offsets, and the packed-mode ambiguity warning. Removed: the worked `transfer` selector value and all `cast` commands (Foundry docs not read).
Method: documentation only; no commands were run.
