---
id: computing-software.blockchain-and-web3.wallets-and-keys.personal-sign-and-message-verification
name: personal-sign-and-message-verification
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [personal-sign, eip191-message, verify-message, bc-wal-signing]
level: practitioner
status: draft
description: "Sign and verify text messages with the EIP-191 prefix and avoid signing raw hashes."
sources:
  - https://eips.ethereum.org/EIPS/eip-191
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# personal_sign
- `personal_sign` hashes `"\x19Ethereum Signed Message:\n" + len(message) + message`, so a signature cannot be reused as a transaction signature.
- Verify off-chain: `ethers.verifyMessage(msg, sig)` or `cast wallet verify --address <a> "msg" <sig>`.
- Never ask users to `eth_sign` a raw hash: it can be a disguised transaction hash.
- For logins, use Sign-In with Ethereum (EIP-4361): includes domain, nonce, issued-at and expiry that the server must check.
- Contract wallets verify via ERC-1271 `isValidSignature(hash, sig)` returning `0x1626ba7e`.

## Verify
- [ ] Server rejects a login signature with a stale nonce or different domain.
