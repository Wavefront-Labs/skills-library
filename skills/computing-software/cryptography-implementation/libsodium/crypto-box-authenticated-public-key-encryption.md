---
id: computing-software.cryptography-implementation.libsodium.crypto-box-authenticated-public-key-encryption
name: crypto-box-authenticated-public-key-encryption
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-box, crypto-box-easy, x25519, xsalsa20-poly1305, sender-authentication, repudiable, public-key-encryption]
level: practitioner
status: verified
description: "Encrypt between two key pairs with crypto_box_easy: repudiable mutual authentication, nonces, no forward secrecy, and when to use sealed boxes or signatures."
sources: ["https://doc.libsodium.org/public-key_cryptography/authenticated_encryption", "https://nacl.cr.yp.to/box.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_box: authenticated public-key encryption

`crypto_box_easy` encrypts a message from Alice to Bob using Alice's secret key
and Bob's public key. Internally: X25519 shared secret -> HSalsa20 -> key for
XSalsa20-Poly1305. Bob decrypts with his secret key and Alice's public key,
and success proves the message came from someone holding Alice's secret key
**or Bob's** (the shared key is symmetric).

```c
unsigned char a_pk[crypto_box_PUBLICKEYBYTES], a_sk[crypto_box_SECRETKEYBYTES];
crypto_box_keypair(a_pk, a_sk);   /* Bob does the same */
unsigned char nonce[crypto_box_NONCEBYTES]; randombytes_buf(nonce, sizeof nonce);
unsigned char c[crypto_box_MACBYTES + mlen];
crypto_box_easy(c, m, mlen, nonce, b_pk, a_sk);              /* Alice -> Bob */
if (crypto_box_open_easy(out, c, sizeof c, nonce, a_pk, b_sk) != 0) { /* reject */ }
```

## Properties to understand

- **Mutual, repudiable authentication**: Bob knows Alice sent it, but cannot
  prove that to a third party (he could have created it himself). Good for
  private messaging; wrong for audit/non-repudiation - sign instead.
- **No forward secrecy**: compromise of either long-term secret key decrypts
  all past messages between them. For sessions, use ephemeral keys
  (`crypto_kx` to derive session keys, or a protocol like Noise).
- **Nonce**: 24 bytes (`crypto_box_NONCEBYTES`, MACBYTES 16, `crypto_box_SEALBYTES` 48); random per message is fine. The same nonce must never
  be reused for the same key pair in either direction - with random nonces
  that is automatic.
- **Key-compromise impersonation**: if Bob's secret key leaks, attackers can
  forge messages "from Alice" to Bob.

## Choosing among box-like APIs

| Need | API |
|---|---|
| Both parties have key pairs, sender authentication to recipient | `crypto_box_easy` |
| Anonymous sender (drop box, telemetry) | `crypto_box_seal` |
| Many messages between same pair | `crypto_box_beforenm` + `_easy_afternm` |
| Proof of origin to third parties | `crypto_sign` (+ encrypt) |
| Interactive session with forward secrecy | `crypto_kx` + AEAD, or Noise |

## Verify

- [ ] Public keys exchanged/verified through a trusted channel (fingerprints).
- [ ] Done on libsodium.js 1.0.22: a box made with Alice's secret and Bob's public key opens with either (Bob secret + Alice public) or (Alice secret + Bob public), which is why the authentication is mutual and repudiable.
- [ ] Decrypt failure handled as rejection; output unused.
- [ ] Forward secrecy requirement assessed; ephemeral design used if needed.
