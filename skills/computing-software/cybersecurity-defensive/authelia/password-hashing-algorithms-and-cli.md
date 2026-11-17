---
id: computing-software.cybersecurity-defensive.authelia.password-hashing-algorithms-and-cli
name: password-hashing-algorithms-and-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, argon2, argon2id, scrypt, pbkdf2, bcrypt, sha2crypt, password-hash, crypto-hash]
level: advanced
status: docs-checked
description: "Choose Authelia password hashing parameters for the file backend and generate or validate digests with authelia crypto hash."
sources:
  - https://www.authelia.com/configuration/first-factor/file/
  - https://www.authelia.com/reference/cli/authelia/authelia_crypto_hash_generate_argon2/
  - https://www.authelia.com/reference/cli/authelia/authelia_crypto_hash_validate/
  - https://www.authelia.com/reference/guides/passwords/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`authentication_backend.file.password.algorithm` picks how new hashes are made: `argon2`, `scrypt`, `pbkdf2`, `sha2crypt` or `bcrypt`. The algorithm applies to newly generated hashes.

Defaults shown in the configuration reference:

```yaml
password:
  algorithm: 'argon2'
  argon2:
    variant: 'argon2id'
    iterations: 3
    memory: 65536
    parallelism: 4
    key_length: 32
    salt_length: 16
```

Others: scrypt iterations 16, block size 8; PBKDF2 `sha512` with 310000 iterations; SHA2Crypt `sha512` with 50000 iterations; bcrypt cost 12. Argon2 `memory` is in kibibytes, and the docs call Argon2 one of the few algorithms designed purely for password hashing, with `argon2id` the recommended variant.

Generate a digest:

```bash
authelia crypto hash generate argon2 --random
authelia crypto hash generate argon2 --profile low-memory
```

Flags include `-i` iterations (3), `-m` memory (65536), `-p` parallelism (4), `-k` key size (32), `-s` salt size (16), `-v` variant and `--profile` (`low-memory` or `recommended`). Without `--password` or `--random` you are prompted, and `--no-confirm` skips the confirmation prompt.

Check a digest against a password with `authelia crypto hash validate --password 'example-only' -- '<DIGEST>'`.

The passwords reference guide advises tuning so one hash takes roughly 500 ms on your hardware, discourages bcrypt except for legacy interoperability, names PBKDF2 as practically the only FIPS 140 choice, and keeps SHA2 Crypt (`sha512`) mainly for backwards compatibility. Its Argon2 suggestions (RFC 9106 based, salt 16, key 32) are `low memory`: argon2id, t=3, p=4, m=65536; `recommended`: argon2id, t=1, p=4, m=2097152. For SHA2 Crypt: 50000 rounds standard, 150000 high end. Hash prefixes identify the algorithm (`$argon2id$`, `$scrypt$`, `$y$` for yescrypt, `$pbkdf2-sha512$`, `$5$`/`$6$`, `$2b$`). PBKDF2 default iterations vary by variant (sha512 310000, sha256 700000).

Memory is released by Go after hashing but the OS may not reclaim it at once, so memory use can look higher than it is. Raise memory cost only if the host can afford it. `--random` defaults to a 72-character alphanumeric password.

Check: validate the generated digest, then log in through the portal.

## Checked

2026-11-08. Read in full: first-factor/file, reference/guides/passwords, CLI pages for crypto hash generate argon2 and crypto hash validate. Added the guide's recommended parameters and algorithm advice.

Method: documentation only; no commands were run.
