---
id: computing-software.cryptography-implementation.openssl.genpkey-algorithm-options
name: genpkey-algorithm-options
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, genpkey, openssl-pkey, genpkey-options, rsa-pss, ec-keys, ml-dsa, openssl-3]
level: practitioner
status: verified
description: "Generate every key type with openssl genpkey: RSA bits and exponent, RSA-PSS restricted keys, EC named curves, Ed25519/X25519, DH groups and OpenSSL 3.5 PQC keys."
sources: ["https://docs.openssl.org/3.0/man1/openssl-genpkey/", "https://docs.openssl.org/master/man7/EVP_PKEY-RSA/", "https://docs.openssl.org/master/man7/EVP_PKEY-EC/", "https://docs.openssl.org/3.5/man7/EVP_PKEY-ML-DSA/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openssl genpkey algorithm options

`genpkey` replaces `genrsa`, `ecparam -genkey`, `gendsa` and `dhparam` with one interface.
Options go through `-pkeyopt name:value`; names are per algorithm (see `EVP_PKEY-<ALG>(7)`).

## RSA
```
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out rsa.key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 \
  -pkeyopt rsa_keygen_pubexp:65537 -out rsa4k.key
```
Keep e = 65537. 2048 is the floor; prefer 3072 or more for new long-lived keys.
`rsa_keygen_primes:2` is the default; multi-prime keys interoperate poorly.

## RSA-PSS restricted key
A key whose OID is `id-RSASSA-PSS` can only be used for PSS, optionally with fixed parameters:
```
openssl genpkey -algorithm RSA-PSS -pkeyopt rsa_keygen_bits:3072 \
  -pkeyopt rsa_pss_keygen_md:sha256 -pkeyopt rsa_pss_keygen_mgf1_md:sha256 \
  -pkeyopt rsa_pss_keygen_saltlen:32 -out pss.key
```
Some TLS stacks and HSMs may not accept RSA-PSS OID certificates; use a plain RSA key with PSS padding
unless you control every verifier.

## Elliptic curves
```
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
  -pkeyopt ec_param_enc:named_curve -out ec.key
openssl ecparam -list_curves           # names OpenSSL knows
```
Always `named_curve` (the default in 3.x; a test key printed `ASN1 OID: prime256v1`); explicit-parameter keys are
rejected by many verifiers. P-256 / P-384 for broad interop,
secp256k1 only for blockchain work.

## Edwards and Montgomery
```
openssl genpkey -algorithm ED25519 -out ed.key
openssl genpkey -algorithm X25519  -out x.key      # key agreement only
openssl genpkey -algorithm ED448   -out ed448.key
```
No options; the key is a 32/57-byte seed.

## Finite-field DH
Prefer named RFC 7919 groups over generating parameters:
```
openssl genpkey -algorithm DH -pkeyopt group:ffdhe3072 -out dh.key
openssl genpkey -genparam -algorithm DH -pkeyopt group:ffdhe3072 -out dhparams.pem
```
Generating custom primes (`dh_paramgen_prime_len`) takes minutes and gains nothing.

## Post-quantum (OpenSSL 3.5+)
```
openssl genpkey -algorithm ML-DSA-65 -out mldsa.key
openssl genpkey -algorithm ML-KEM-768 -out mlkem.key
openssl genpkey -algorithm SLH-DSA-SHA2-128s -out slh.key
openssl list -key-managers | grep -i ml-     # confirm support
```
ML-KEM/ML-DSA private keys may be written as seed, expanded key, or both; the provider's
`ml-kem.output_formats` / `ml-dsa.output_formats` settings control it. Per the 3.5 manual the default writes both seed
and key (`seed-priv`) when the seed is known; listing `seed-only` first writes the smallest form. Algorithm names and
these settings are from the OpenSSL 3.5 manual; they were not run here (OpenSSL 3.2.3 rejects `ML-DSA-65`).

## Useful common flags
- `-out key.pem` then `chmod 600`; or encrypt on creation with `-aes-256-cbc -pass file:pw.txt`.
- `-text` prints components; `-quiet` suppresses progress dots.
- `-provider fips` / `-propquery fips=yes` to generate inside the FIPS provider (needs an installed and configured FIPS module).

## Verify
- [ ] `openssl pkey -in key.pem -noout -text` shows the intended algorithm, size/curve.
- [ ] EC keys show `ASN1 OID: prime256v1` (named), not explicit parameters.
- [ ] Private key files are mode 600 or encrypted.
