---
id: computing-software.cryptography-implementation.openssl.legacy-genrsa-and-rsa-commands
name: legacy-genrsa-and-rsa-commands
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-genrsa, openssl-rsa, pkcs1, pkcs8, openssl-3, genpkey]
level: practitioner
status: verified
description: "Handle legacy openssl genrsa and rsa commands in OpenSSL 3: PKCS#8 output by default, -traditional for PKCS#1, deprecation warnings, and genpkey replacements."
sources: ["https://docs.openssl.org/3.0/man1/openssl-genrsa/", "https://docs.openssl.org/3.0/man1/openssl-rsa/", "https://docs.openssl.org/3.0/man7/migration_guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy genrsa and rsa commands

## What changed in OpenSSL 3
- `openssl genrsa` still works but writes PKCS#8 (`-----BEGIN PRIVATE KEY-----`) instead of PKCS#1
  (`-----BEGIN RSA PRIVATE KEY-----`). Add `-traditional` for the old format.
- Default size is 2048; the size is now the last argument (`openssl genrsa -out k.pem 3072`).
- `openssl rsa` likewise outputs PKCS#8 unless `-traditional`; `-RSAPublicKey_out` writes PKCS#1 public keys.
- `-des`, `-des3` options remain but use AES (`-aes256`) for encrypted keys.

## Replacements
```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out k.pem
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -aes-256-cbc -out k.pem
openssl pkey -in k.pem -traditional -out k-pkcs1.pem     # for tools needing PKCS#1
openssl pkey -in k.pem -pubout -out pub.pem
```

## Why it matters
Older tools and libraries that only parse PKCS#1 expect `RSA PRIVATE KEY` headers and fail on PKCS#8; check the
consumer's documentation. Scripts that grep for the header break after upgrading.

Tested on OpenSSL 3.2.3: `genrsa`, `rsa` and `pkey` write `BEGIN PRIVATE KEY` by default and `BEGIN RSA PRIVATE KEY`
with `-traditional`; `genrsa` with no size makes a 2048-bit key; `-des3`/`-aes256` still work; `-RSAPublicKey_out` writes
`BEGIN RSA PUBLIC KEY`.

## Verify
- [ ] `head -1 k.pem` shows the header the consumer expects.
- [ ] `openssl pkey -in k.pem -check -noout` reports the key valid.
