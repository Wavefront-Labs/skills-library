---
id: computing-software.blockchain-and-web3.smart-contract-security.signature-replay-protection
name: signature-replay-protection
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [signature-replay, nonce-in-signature, swc-121, bc-sec-signatures]
level: practitioner
status: draft
description: "Bind signatures to a nonce, deadline, chain and contract so they cannot be replayed."
sources:
  - https://swcregistry.io/
  - https://eips.ethereum.org/EIPS/eip-712
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replay protection
A signed message must commit to everything that makes it valid exactly once:
- The signer's nonce (increment on use) or a unique id marked used.
- A deadline.
- `chainId` and `verifyingContract` (EIP-712 domain separator).
- The exact parameters (amount, recipient, function).
Common bugs: no nonce; nonce shared across message types; domain separator cached at deployment but contract is behind a chain fork (recompute if `block.chainid` changed); hashing `abi.encodePacked` with multiple dynamic fields.

## Verify
- [ ] Submitting the same signature twice, or on another chain's fork, reverts.
