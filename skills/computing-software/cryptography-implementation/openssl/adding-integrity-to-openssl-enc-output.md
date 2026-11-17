---
id: computing-software.cryptography-implementation.openssl.adding-integrity-to-openssl-enc-output
name: adding-integrity-to-openssl-enc-output
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, enc-integrity-check, openssl-enc, encrypt-then-mac, hmac, openssl-mac]
level: practitioner
status: verified
description: "Add integrity to openssl enc ciphertext, which is unauthenticated CBC/CTR: encrypt-then-MAC with openssl mac or dgst -hmac, separate keys, and verifying before decrypt."
sources: ["https://docs.openssl.org/3.0/man1/openssl-enc/", "https://docs.openssl.org/3.0/man1/openssl-mac/", "https://docs.openssl.org/3.0/man1/openssl-dgst/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding integrity to openssl enc output

`openssl enc` does not support AEAD modes (`openssl enc -aes-256-gcm` prints `AEAD ciphers not supported`) and produces unauthenticated ciphertext. Tampering goes
undetected; padding errors can act as an oracle. Prefer `age` or `openssl cms -aes-256-gcm`. If `enc` must be used,
add encrypt-then-MAC.

## Script
```sh
# keys: 32-byte encryption and 32-byte MAC keys, separate
EK=$(openssl rand -hex 32); MK=$(openssl rand -hex 32); IV=$(openssl rand -hex 16)
openssl enc -aes-256-ctr -K "$EK" -iv "$IV" -in data.bin -out data.enc
# needs xxd (ships with vim; present in Git for Windows)
{ printf %s "$IV" | xxd -r -p; cat data.enc; } > data.ivct
openssl mac -digest SHA256 -macopt hexkey:"$MK" -in data.ivct -binary HMAC > data.tag

# verify then decrypt
openssl mac -digest SHA256 -macopt hexkey:"$MK" -in data.ivct -binary HMAC | cmp -s - data.tag || exit 1
tail -c +17 data.ivct | openssl enc -d -aes-256-ctr -K "$EK" -iv "$IV" -out data.out
```

Tested on OpenSSL 3.2.3: the script round-trips, and `openssl mac` prints its MAC name last (`HMAC` after `-in`).

## Rules
- MAC the IV and the ciphertext (and a version/header if any).
- Separate keys for encryption and MAC, or derive both from one master with `openssl kdf ... HKDF`.
- Verify the tag before decrypting anything. `cmp` is not constant time; acceptable for local file checks, not
  for network-facing services.
- With password-based keys, derive via `-pbkdf2 -iter 600000` and still MAC with a separately derived key.

## Verify
- [ ] Flipping one byte of `data.ivct` makes verification fail before decryption.
