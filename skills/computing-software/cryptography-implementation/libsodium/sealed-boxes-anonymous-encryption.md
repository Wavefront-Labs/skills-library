---
id: computing-software.cryptography-implementation.libsodium.sealed-boxes-anonymous-encryption
name: sealed-boxes-anonymous-encryption
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-box, sealed-box, crypto-box-seal, anonymous-sender, ephemeral-key, github-secrets-api, drop-box]
level: practitioner
status: docs-checked
description: "Encrypt to a public key without a sender identity using crypto_box_seal: 48-byte overhead, no sender authentication, typical uses (GitHub secrets API, telemetry), and pitfalls."
sources: ["https://doc.libsodium.org/public-key_cryptography/sealed_boxes", "https://github.com/github/docs/blob/main/content/rest/guides/encrypting-secrets-for-the-rest-api.md", "https://pynacl.readthedocs.io/en/latest/public/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sealed boxes: anonymous public-key encryption

`crypto_box_seal` encrypts to a recipient's X25519 public key using a fresh
ephemeral key pair per message. Only the recipient can decrypt; nobody,
including the sender afterwards, can - the ephemeral secret is erased.

```c
unsigned char c[crypto_box_SEALBYTES + mlen];          /* SEALBYTES = 48 */
crypto_box_seal(c, m, mlen, recipient_pk);
if (crypto_box_seal_open(out, c, sizeof c, recipient_pk, recipient_sk) != 0) { /* reject */ }
```

Layout (libsodium docs): `ephemeral_pk` followed by `box(m, recipient_pk, ephemeral_sk, nonce=blake2b(ephemeral_pk || recipient_pk))`, built on crypto_box (X25519 and XSalsa20-Poly1305), so there is no
nonce to manage. `crypto_box_SEALBYTES` is the public key size plus the MAC size (32 + 16).

PyNaCl: `SealedBox(recipient_public_key).encrypt(msg)` /
`SealedBox(private_key).decrypt(ct)`. libsodium.js:
`crypto_box_seal(msg, pk)` (as in GitHub's example) and `crypto_box_seal_open`, since its API mirrors the C library.

## Common uses

- Uploading secrets to a service that publishes a public key: the GitHub REST API's secrets endpoints require values encrypted with libsodium; GitHub's guide uses `crypto_box_seal` with the base64 public key it returns.
- Anonymous submissions: the docs describe sealed boxes as designed to send messages anonymously to a recipient, and the message cannot be correlated with its sender without additional data.
- Write-only components: a front end encrypts records that only a back-office
  key can read.

## Pitfalls

- **No sender authentication**: anyone with the public key can create valid
  sealed boxes. If the recipient must know who sent it, sign the plaintext
  inside (or use `crypto_box_easy` / HPKE auth mode).
- **No forward secrecy for the recipient**: only the recipient's key is needed to open a box, so compromise of `recipient_sk`
  decrypts all past sealed boxes to it. Rotate recipient keys and keep their
  lifetime bounded.
- Replay: the same sealed box can be resubmitted; include ids/timestamps
  inside if it matters.
- Recipient must use the same libsodium construction; the format above is specific to crypto_box_seal.

## Verify

- [ ] Ciphertext length = message + 48.
- [ ] Recipient verifies sender identity separately where needed.
- [ ] Recipient key rotation plan exists.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: crypto_box_seal and crypto_box_seal_open signatures, ciphertext length of crypto_box_SEALBYTES plus the message, ephemeral key pair erased after encryption, sealed box format and nonce derivation, recipient cannot verify the sender (docs); crypto_box_SEALBYTES is the public key size plus MAC size (header); GitHub REST guide (libsodium, crypto_box_seal, base64 key); PyNaCl SealedBox. Removed an unconfirmed claim about HPKE and ECIES interoperability and telemetry as a named use.

Method: documentation only; no commands were run.
