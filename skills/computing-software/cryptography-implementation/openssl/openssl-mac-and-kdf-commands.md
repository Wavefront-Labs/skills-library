---
id: computing-software.cryptography-implementation.openssl.openssl-mac-and-kdf-commands
name: openssl-mac-and-kdf-commands
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-dgst, openssl-mac-kdf, openssl-mac, openssl-kdf, hmac, hkdf, cmac, kmac, test-vectors, openssl-3]
level: practitioner
status: verified
description: "Compute HMAC, CMAC, KMAC and derive keys with HKDF, PBKDF2, scrypt or SSKDF using the OpenSSL 3 mac and kdf commands, e.g. to cross-check application output."
sources: ["https://docs.openssl.org/3.0/man1/openssl-mac/", "https://docs.openssl.org/3.0/man1/openssl-kdf/", "https://docs.openssl.org/3.0/man7/EVP_KDF-HKDF/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# openssl mac and kdf commands

OpenSSL 3 added `openssl mac` and `openssl kdf`, which expose EVP_MAC and
EVP_KDF. They are the quickest way to produce reference values when debugging
an application's HMAC or HKDF output.

## MACs

```bash
# HMAC-SHA256, key as hex
openssl mac -digest SHA256 -macopt hexkey:000102030405060708090a0b0c0d0e0f -in msg.bin HMAC
# CMAC with AES-128
openssl mac -cipher AES-128-CBC -macopt hexkey:2b7e151628aed2a6abf7158809cf4f3c -in msg.bin CMAC
# KMAC256 with customisation string
openssl mac -macopt hexkey:<64 hex chars> -macopt custom:"app v1" -macopt size:32 -in msg.bin KMAC-256
```

Output is uppercase hex; `-binary` for raw bytes. The MAC name (`HMAC`, `CMAC`, `KMAC-256`) must be the **last** argument, after `-in`: `openssl mac ... HMAC -in f` fails with "Extra argument after MAC name" (checked on 3.2.3). The older
`openssl dgst -sha256 -hmac key` form works but takes the key as a text
string, which hides encoding mistakes; use `-mac HMAC -macopt hexkey:` with dgst or the mac command.

## KDFs

```bash
# HKDF-SHA256 (extract+expand), 32 bytes
openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt hexkey:<ikm hex> \
  -kdfopt hexsalt:<salt hex> -kdfopt info:"app v1 enc" HKDF
# Expand-only
openssl kdf -keylen 32 -kdfopt mode:EXPAND_ONLY -kdfopt digest:SHA256 -kdfopt hexkey:<prk> -kdfopt info:ctx HKDF
# PBKDF2
openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt pass:"correct horse" \
  -kdfopt hexsalt:<16-byte salt hex> -kdfopt iter:600000 PBKDF2
# scrypt
openssl kdf -keylen 32 -kdfopt pass:pw -kdfopt hexsalt:<salt> -kdfopt n:131072 -kdfopt r:8 -kdfopt p:1 SCRYPT
# SP 800-56C one-step (SSKDF) and SP 800-108 (KBKDF) also available
openssl kdf -keylen 32 -kdfopt mac:HMAC -kdfopt digest:SHA256 -kdfopt hexkey:<k> -kdfopt hexsalt:<label> -kdfopt hexinfo:<context> KBKDF
```

`openssl list -kdf-algorithms` and `-mac-algorithms` show what your build and
providers offer (FIPS provider restricts these).

## Use for debugging

1. Dump the exact bytes your application uses (key, salt, info) as hex.
2. Run the OpenSSL command with `hex*` options.
3. Compare. Most mismatches are encoding: text vs hex key, UTF-8 vs UTF-16
   info strings, missing salt treated as zero-length vs hash-length zeros
   (equivalent in HKDF), or base64 key decoded twice.

Tested on 3.2.3: the HMAC-SHA256 command reproduces RFC 4231 test case 1, the HKDF command reproduces RFC 5869 test
case 1 (output `3C:B2:5F:25:...:58:65`, colon-separated hex for `openssl kdf` without `-binary`), `CMAC`, `KMAC-256`,
`PBKDF2`, `SCRYPT`, `KBKDF`, `SSKDF` and `X963KDF` run, and HKDF with no salt equals HKDF with a 32-byte zero salt.

## Verify

- [ ] RFC 4231 HMAC and RFC 5869 HKDF test case 1 reproduce with these commands.
- [ ] Application outputs match OpenSSL for the same hex inputs.
