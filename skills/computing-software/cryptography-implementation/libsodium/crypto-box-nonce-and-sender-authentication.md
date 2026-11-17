---
id: computing-software.cryptography-implementation.libsodium.crypto-box-nonce-and-sender-authentication
name: crypto-box-nonce-and-sender-authentication
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-box-nonce, crypto-box, libsodium, nonce-reuse, sender-authentication, repudiation, kci, public-key-encryption]
level: advanced
status: verified
description: "Use crypto_box safely: the shared key means nonces must be unique across both directions, what sender authentication does and does not give, and repudiability."
sources: ["https://doc.libsodium.org/public-key_cryptography/authenticated_encryption", "https://nacl.cr.yp.to/box.html", "https://doc.libsodium.org/public-key_cryptography/sealed_boxes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_box nonces and sender authentication

`crypto_box_easy(c, m, mlen, nonce, recipient_pk, sender_sk)` computes X25519(sender_sk, recipient_pk), derives a
symmetric key, and uses XSalsa20-Poly1305 (libsodium docs: X25519 key exchange, XSalsa20, Poly1305). Both parties derive the **same** key (checked: one box opened with both key combinations).

## Nonce rule
Because Alice-to-Bob and Bob-to-Alice use the same shared key, a nonce used by Alice must never be used by Bob
either. Options:
- Random 24-byte nonces for every message (simplest, safe).
- Counters with a direction bit: Alice uses even nonces, Bob odd; or the first byte identifies the sender.
- Lexicographic rule: the party with the smaller public key uses one half of the space.

## What sender authentication means here
- Bob knows the message came from someone holding Alice's secret key **or Bob's own secret key**. Bob can create a
  box that looks like it came from Alice: authentication is symmetric and messages are **repudiable** (Bob cannot
  prove to a third party that Alice sent it).
- If Bob's secret key leaks, an attacker can impersonate anyone to Bob (key-compromise impersonation).
- There is no forward secrecy: a later leak of either long-term key decrypts all past boxes between them.

## When to use something else
| Need | Use |
|---|---|
| Anonymous sender | `crypto_box_seal` |
| Non-repudiable sender | Sign with `crypto_sign` then box, or sign-then-seal with recipient bound into the signed data |
| Forward secrecy | Ephemeral keys per session (`crypto_kx` with ephemeral keypairs authenticated by signatures) |
| Many messages to one peer | `crypto_box_beforenm` once, then `crypto_box_easy_afternm` |

## Verify
- [ ] Nonce scheme guarantees uniqueness across both directions (test both parties sending simultaneously).
- [ ] Threat model accepts repudiability and lack of forward secrecy, or the design adds them.
