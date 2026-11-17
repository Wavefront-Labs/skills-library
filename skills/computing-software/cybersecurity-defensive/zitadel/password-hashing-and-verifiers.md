---
id: computing-software.cybersecurity-defensive.zitadel.password-hashing-and-verifiers
name: password-hashing-and-verifiers
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, password-hashing, bcrypt, argon2, migration, verifiers]
level: advanced
status: docs-checked
description: "Check which password hash algorithms ZITADEL supports, why only bcrypt is enabled by default, and how hashes are upgraded after a successful login."
sources:
  - https://zitadel.com/docs/concepts/architecture/secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL hashes all passwords and client secrets irreversibly, with a random salt. The stored string is an encoded value containing the algorithm, its parameters, the salt and the hash, in Modular Crypt Format. The encoding is implemented by the Passwap library.

Supported algorithms: argon2i and argon2id, bcrypt (the default), md5 variants (md5Crypt, md5plain, md5salted), phpass as used by WordPress, drupal7, sha2 (crypt SHA-256 and SHA-512), scrypt and pbkdf2.

Two behaviors matter when you migrate users:

- You can import passwords from systems using any of these algorithms.
- By default only bcrypt is enabled. The other verifiers must be enabled by the system administrator in the runtime configuration before such imported hashes will validate.

When you change the configured algorithm or its cost parameters, ZITADEL rewrites a stored hash the first time the user's verification succeeds. That lets you raise cost over time without forcing resets.

md5 variants and drupal7 are insecure and can only be used to import and verify users, not to hash new passwords. The argon2 algorithms are disabled on ZITADEL Cloud because of their memory requirements.

## Checked

2026-11-08. Read the secrets page in full; replaced an invented migration order with the documented insecure-algorithm and Cloud argon2 notes.

Method: documentation only; no commands were run.
