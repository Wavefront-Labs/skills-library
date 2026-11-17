---
id: computing-software.cryptography-implementation.openssl.validating-keys-with-pkey-check
name: validating-keys-with-pkey-check
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pkey-check, openssl-pkey, key-validation, rsa, ecdsa, pubcheck]
level: practitioner
status: verified
description: "Validate private and public keys with openssl pkey -check and -pubcheck: RSA consistency, EC point validation, DH parameter checks, and limits of what they prove."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkey/", "https://docs.openssl.org/3.0/man3/EVP_PKEY_check/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating keys with pkey -check

```sh
openssl pkey -in key.pem -check -noout          # full private key check
openssl pkey -pubin -in pub.pem -pubcheck -noout # public key check
openssl pkeyparam -in dhparam.pem -check -noout  # DH/EC parameters
```
Output `Key is valid` or an error such as `p not prime`, `d e not congruent to 1`, `point is not on curve`. Tested on
3.2.3: RSA, EC and Ed25519 keys and DH/EC parameters print valid/`Parameters are valid`; an RSA key with a corrupted CRT
value printed `iqmp not inverse of q` and `Key is invalid`.

## What is checked (EVP_PKEY_check family)
- RSA: p and q prime, n = p*q, d*e = 1 mod lcm(p-1, q-1), CRT values consistent. Per the `EVP_PKEY_check` manual the FIPS
  provider follows SP 800-56A/B; the default provider "may use checks that are not as restrictive" for some key types.
- EC: private scalar in range, public point on curve, not infinity, matches private key, order check.
- DH: parameters (safe prime if known group), public value in range.
- `-pubcheck` (public only): EC point validity, RSA modulus sanity; cannot prove factorization correctness.

## Use cases
- After importing keys from another system or HSM export.
- Before accepting customer-supplied keys (BYOK) or peer public keys in protocols.
- Detecting corrupted keys from bad conversions.

## Limits
- Does not detect weak but valid keys; a dedicated checker such as `badkeys` ("checks cryptographic public keys for
  known vulnerabilities", per its README) covers that.
- `EVP_PKEY_check` is an alias of `EVP_PKEY_pairwise_check`, and the manual warns that the private and pairwise checks
  might not be bounded by key-size limits, so do not run them on untrusted large keys.

## Verify
- [ ] CI step runs `-check` on generated keys; failures stop deployment.
