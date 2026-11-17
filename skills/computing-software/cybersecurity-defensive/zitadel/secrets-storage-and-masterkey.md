---
id: computing-software.cybersecurity-defensive.zitadel.secrets-storage-and-masterkey
name: secrets-storage-and-masterkey
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, secrets, masterkey, encryption, aes256, key-management]
level: advanced
status: docs-checked
description: "Understand how ZITADEL hashes, encrypts and stores secrets, and why the 32-byte masterkey must be protected outside the database."
sources:
  - https://zitadel.com/docs/concepts/architecture/secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL treats secrets by principle: automate rotation, limit lifetime, show only once, prefer public/private key mechanisms (FIDO2, U2F, JWT profile), hash irreversibly, encrypt storage, and force a change plus single use for secrets sent over insecure channels such as email or SMS.

By default secrets of users and applications, and generated secrets such as signing keys, are kept in the database. They are encrypted with AES256. The key is the `masterkey`, which must be exactly 32 bytes long. The only secrets stored outside this storage are the masterkey, the TLS keys and the initial admin user including its password.

Storage categories:

- Public keys (FIDO2, U2F, JWT profile, signing keys) are protected from tampering by the eventstore.
- Hashed secrets: passwords and client secrets, hashed with a random salt.
- Encrypted secrets that must be usable in raw form: identity provider client secrets, TOTP seeds and validation secrets for email, phone and DNS ownership.

Because the masterkey protects the secrets storage it cannot live inside it; the configuration docs list the ways ZITADEL can consume it. Encryption is meant to protect against extraction from the database and from database dumps. By default RSA256 is used for signing and AES256 for encryption. The initial admin user is forced to change its password at first login.

## Checked

2026-11-08. Read the secrets page in full; replaced operational advice not on the page with documented facts.

Method: documentation only; no commands were run.
