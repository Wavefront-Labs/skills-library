---
id: computing-software.blockchain-and-web3.smart-contract-security.ecdsa-malleability-and-ecrecover
name: ecdsa-malleability-and-ecrecover
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [ecrecover-pitfalls, signature-malleability, zero-address-recover]
level: practitioner
status: draft
description: "Use ECDSA.recover instead of raw ecrecover: reject high-s signatures and the zero-address result."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/api/utils#ECDSA
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ecrecover pitfalls
- `ecrecover` returns `address(0)` for an invalid signature; comparing against an unset signer address of zero would accept it. Always require non-zero signer.
- Each valid signature (r, s, v) has a second valid form (r, n-s, v flipped). If you use the signature bytes (not a nonce) as a uniqueness key, malleability allows double use. Use OpenZeppelin `ECDSA`, which rejects high-s values.
- For contract wallets use ERC-1271 `isValidSignature` (`SignatureChecker`).
- Hash a structured message with EIP-712 rather than raw strings.

## Verify
- [ ] Test: flipped-s signature is rejected; zero signer is rejected.
