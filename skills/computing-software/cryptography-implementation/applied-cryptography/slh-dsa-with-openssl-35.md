---
id: computing-software.cryptography-implementation.applied-cryptography.slh-dsa-with-openssl-35
name: slh-dsa-with-openssl-35
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, openssl-slh-dsa, slh-dsa, fips-205, sphincs-plus, openssl, hash-based-signatures]
level: advanced
status: docs-checked
description: "Generate, sign and verify with SLH-DSA (FIPS 205) in OpenSSL 3.5: algorithm names, pure versus pre-hash, context strings, signature sizes and speed tradeoffs."
sources: ["https://docs.openssl.org/3.5/man7/EVP_PKEY-SLH-DSA/", "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf", "https://docs.openssl.org/3.5/man7/EVP_SIGNATURE-SLH-DSA/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLH-DSA with OpenSSL 3.5

## Algorithm names
`SLH-DSA-SHA2-128s`, `-128f`, `-192s`, `-192f`, `-256s`, `-256f`, and the `SHAKE` equivalents.
`s` = smaller signatures, much slower; `f` = faster, larger signatures.
There are 12 sets in all (SHA2 and SHAKE at 128, 192, 256 bits, each s and f).

| Set | pk | sig |
|---|---|---|
| SHA2-128s | 32 B | 7856 B |
| SHA2-128f | 32 B | 17088 B |
| SHA2-256s | 64 B | 29792 B |

Public keys are 32, 48 or 64 bytes for 128, 192, 256. Other signature sizes: 192s 16224 B, 192f 35664 B, 256f 49856 B.

## Commands
```sh
openssl genpkey -algorithm SLH-DSA-SHA2-128s -out slh.pem
openssl pkey -in slh.pem -pubout -out slh.pub
openssl pkeyutl -sign -inkey slh.pem -rawin -in msg.bin -out msg.sig
openssl pkeyutl -verify -pubin -inkey slh.pub -rawin -in msg.bin -sigfile msg.sig
openssl pkeyutl -sign -inkey slh.pem -rawin -in msg.bin -pkeyopt context-string:myapp-v1 -out m.sig
```
`-rawin` is required: SLH-DSA signs the message itself (pure mode). No `-digest`.

## Notes
- SLH-DSA has relatively large signatures and is slow compared with ML-DSA; suit it to firmware, roots and
  long-lived signatures rather than TLS handshakes.
- Deterministic signing option: `-pkeyopt deterministic:1` uses the private key seed; default draws randomness
  from the DRBG.
- Stateless: no state file, unlike LMS/XMSS.
- `context-string` is at most 255 bytes, empty by default.
- OpenSSL does not support Pre Hash SLH-DSA directly; pure mode only.

## Verify
- [ ] Signature from OpenSSL verifies with a second implementation (liboqs, BouncyCastle) for the same set.

## Checked
2026-11-01. Confirmed against OpenSSL 3.5 EVP_PKEY-SLH-DSA(7), EVP_SIGNATURE-SLH-DSA(7), openssl-pkeyutl and openssl-genpkey: parameter set names, key and signature sizes, context string limit, deterministic behaviour, no pre-hash support. Removed signing-time figures and the OID remark (not in the fetched pages).
Method: documentation only; no commands were run.
