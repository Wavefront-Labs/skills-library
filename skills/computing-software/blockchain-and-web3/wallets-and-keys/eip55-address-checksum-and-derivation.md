---
id: computing-software.blockchain-and-web3.wallets-and-keys.eip55-address-checksum-and-derivation
name: eip55-address-checksum-and-derivation
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [eip55-checksum, address-derivation, secp256k1-keys, bc-wal-addresses]
level: practitioner
status: draft
description: "Derive an Ethereum address from a public key and validate EIP-55 mixed-case checksums."
sources:
  - https://eips.ethereum.org/EIPS/eip-55
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ethereum addresses
- Private key: 32 random bytes (secp256k1). Public key: uncompressed 64 bytes (x||y). Address = last 20 bytes of keccak256(pubkey).
- EIP-55: hex-encode the lowercase address; hash that ASCII string with keccak256; for each letter, uppercase it if the corresponding hash nibble is >= 8.
- Validate with `cast to-check-sum-address <addr>` or `ethers.getAddress`. A mixed-case address failing the checksum is likely mistyped; an all-lowercase one carries no checksum.
- Never generate keys with weak randomness (`Math.random`, brainwallets).

## Verify
- [ ] Derivation of the well-known test key reproduces its documented address.
