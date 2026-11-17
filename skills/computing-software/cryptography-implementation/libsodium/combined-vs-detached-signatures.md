---
id: computing-software.cryptography-implementation.libsodium.combined-vs-detached-signatures
name: combined-vs-detached-signatures
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-sign, crypto-sign-detached, crypto-sign-open, ed25519, signatures, signed-message, verify-then-use]
level: practitioner
status: verified
description: "Choose libsodium crypto_sign (combined, signature+message) vs crypto_sign_detached: buffer sizes, verify-then-use with crypto_sign_open, and key/signature encodings."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://datatracker.ietf.org/doc/html/rfc8032", "https://github.com/jedisct1/libsodium/blob/master/ChangeLog"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combined versus detached signatures in libsodium

`crypto_sign_*` is Ed25519: 32-byte public key, 64-byte secret key (seed ||
public key), 64-byte signature, deterministic signing.

## Combined mode

```c
unsigned char pk[crypto_sign_PUBLICKEYBYTES], sk[crypto_sign_SECRETKEYBYTES];
crypto_sign_keypair(pk, sk);
unsigned char sm[crypto_sign_BYTES + mlen]; unsigned long long smlen;
crypto_sign(sm, &smlen, m, mlen, sk);                 /* sm = signature || message */
unsigned char out[mlen]; unsigned long long outlen;
if (crypto_sign_open(out, &outlen, sm, smlen, pk) != 0) { /* reject */ }
/* use only `out`, never the tail of `sm` */
```

`crypto_sign_open` outputs the message only if the signature is valid. This
"verify then use" API makes it hard to act on an unverified message - good for
signed tokens and messages that travel as one blob.

## Detached mode

```c
unsigned char sig[crypto_sign_BYTES];
crypto_sign_detached(sig, NULL, m, mlen, sk);
if (crypto_sign_verify_detached(sig, m, mlen, pk) != 0) { /* reject */ }
```

Use when the message is stored or transmitted separately: signing files,
database rows, HTTP bodies with a signature header, or when you want to avoid
copying a large message.

## Choosing

| Situation | Mode |
|---|---|
| Opaque signed blob (token, packet) | combined + `crypto_sign_open` |
| Artifact + .sig file, HTTP header signature | detached |
| Very large data | detached over a hash? No - use `crypto_sign_init/update/final_create` (Ed25519ph) |

## Pitfalls

- With detached mode, code paths that parse the message before
  `verify_detached` succeeds reintroduce verify-after-use bugs; verify first.
- The 64-byte secret key embeds the public key. Some other libraries store
  only the 32-byte seed; convert with `crypto_sign_seed_keypair` or
  `crypto_sign_ed25519_sk_to_seed`.
- Signatures are not encrypted; anyone can read the message in combined mode.
- libsodium verification rejects non-canonical public key encodings and low-order public keys (since 1.0.16, per the changelog), and a signature whose S was changed to S + L (checked on 1.0.22: verify returns false; a small-order public key also fails). That is stricter than RFC 8032's minimum, so expect rare interop rejects of edge-case signatures from other implementations, which is desired.

## Verify

- [ ] RFC 8032 section 7.1 test 1-3 vectors verify (done: seeds from tests 1, 2 and 3 reproduce the public key and signature with `crypto_sign_seed_keypair` and `crypto_sign_detached`).
- [ ] Modified message or signature returns -1.
- [ ] No message field is used before verification returns 0.
