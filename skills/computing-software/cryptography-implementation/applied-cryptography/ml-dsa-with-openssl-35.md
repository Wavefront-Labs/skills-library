---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-with-openssl-35
name: ml-dsa-with-openssl-35
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, openssl-ml-dsa, ml-dsa, openssl, openssl-3-5, fips-204, pkeyutl, genpkey, post-quantum, signatures]
level: practitioner
status: docs-checked
description: "Create ML-DSA keys, sign and verify files, set context strings and deterministic mode, and issue test certificates with OpenSSL 3.5."
sources: ["https://docs.openssl.org/3.5/man7/EVP_PKEY-ML-DSA/", "https://docs.openssl.org/3.5/man7/EVP_SIGNATURE-ML-DSA/", "https://csrc.nist.gov/pubs/fips/204/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-DSA with OpenSSL 3.5

## Keys and sizes
```
openssl genpkey -algorithm ML-DSA-65 -out mldsa.key
openssl pkey -in mldsa.key -pubout -out mldsa.pub
```
| Set | Public key | Private key (FIPS 204 sk) | Category |
|---|---|---|---|
| ML-DSA-44 | 1312 B | 2560 B | 2 |
| ML-DSA-65 | 1952 B | 4032 B | 3 |
| ML-DSA-87 | 2592 B | 4896 B | 5 |

Signatures range from about 2.5K to about 4.5K bytes depending on the set.

## Sign and verify (pure ML-DSA, whole message)
```
openssl pkeyutl -sign -rawin -inkey mldsa.key -in release.tar -out release.sig
openssl pkeyutl -verify -rawin -pubin -inkey mldsa.pub -in release.tar -sigfile release.sig
```
Options via `-pkeyopt`:
- `context-string:<string>` - FIPS 204 context (at most 255 bytes, empty by default); verifier must pass the same string.
- `deterministic:1` - per-message randomness set to 32 zero bytes (default 0 draws it from the DRBG).
- `message-encoding:0` - skips message encoding and is for testing only; it makes the FIPS indicator return 0.

## Certificates
```
openssl req -x509 -new -key mldsa.key -subj "/CN=pq-test" -days 30 -out mldsa.crt
openssl x509 -in mldsa.crt -noout -text | grep -i "Public Key Algorithm"
```
Check that the peers you need accept ML-DSA certificates before relying on them outside internal tests.

## Gotchas
- Pure ML-DSA signs the whole message, encoded as 0x00 || len(ctx) || ctx || message. OpenSSL does not support
  Pre Hash ML-DSA; the `mu` signature parameter lets you pass the FIPS 204 mu value instead of a raw message, and
  the verifier must use the same variant.
- Private keys are PKCS#8 files that may hold the 32-byte seed, the expanded key, or both. Provider settings
  `ml-dsa.retain_seed`, `ml-dsa.prefer_seed`, `ml-dsa.input_formats` and `ml-dsa.output_formats` control this;
  check import compatibility with HSMs.

## Verify
- [ ] Verification fails when the context string differs.
- [ ] The public key length matches the table for the parameter set.

## Checked
2026-11-01. Confirmed against the OpenSSL 3.5 pages EVP_PKEY-ML-DSA(7), EVP_SIGNATURE-ML-DSA(7), openssl-pkeyutl, openssl-genpkey and openssl-req: key sizes, categories, context-string limit, message-encoding, deterministic, mu, seed formats and provider parameters. Removed exact signature sizes, OIDs, the CNSA 2.0 label, the `dgst` remark and TLS client claims (not in the fetched pages).
Method: documentation only; no commands were run.
