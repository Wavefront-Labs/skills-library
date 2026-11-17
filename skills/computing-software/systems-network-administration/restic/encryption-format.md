---
id: computing-software.systems-network-administration.restic.encryption-format
name: encryption-format
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, encryption, aes-256, poly1305, scrypt, master-key, key-files]
level: sme
status: docs-checked
description: "How restic encrypts and authenticates repository files: AES-256-CTR, Poly1305-AES, the IV and MAC layout and scrypt key derivation."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/design.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption format

Every repository file except the key files is stored as:

```
IV || CIPHERTEXT || MAC
```

with a 16-byte IV and a 16-byte MAC, so 32 bytes overhead per file. A new random IV is used for each file.

## Algorithms

- Encryption: AES-256 in counter mode
- Authentication: Poly1305-AES

## Keys

The master key, stored encrypted in a key file, contains the AES-256 key and the Poly1305 keys (`k`, a 16-byte AES key, and `r`, a masked 16-byte key).

Key files in `keys/` are JSON. They hold the encrypted master key and the scrypt parameters (N, r, p, salt). Restic derives 64 bytes from your password with scrypt, and splits them: bytes 0-31 are the AES-256 key, bytes 32-47 the Poly1305 AES key `k`, and bytes 48-63 the key `r`.

## Consequences

- Several key files can unlock the same master key, so passwords can be added and removed without re-encrypting data.
- A leaked master key exposes all data, and changing the password does not fix that.
- Data is authenticated, so tampering is detected.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/design.rst.

Method: documentation only; no commands were run.
