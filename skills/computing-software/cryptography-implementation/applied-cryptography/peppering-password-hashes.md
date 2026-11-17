---
id: computing-software.cryptography-implementation.applied-cryptography.peppering-password-hashes
name: peppering-password-hashes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, password-hashing, password-pepper, pepper, hmac, secrets-manager, hsm, owasp]
level: advanced
status: docs-checked
description: "Add a pepper to password hashing: pre-hash versus post-hash HMAC, where the pepper lives, and why rotating it forces password resets."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#peppering", "https://pages.nist.gov/800-63-4/sp800-63b.html", "https://csrc.nist.gov/pubs/sp/800/132/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peppering password hashes

A pepper is a secret shared by all stored passwords (unlike a per-password salt), kept outside the database. If only
the database leaks (SQL injection, a backup), the attacker cannot start cracking. It is added on top of salted
password hashing, never a replacement: used alone it adds no secure characteristics.

## Two strategies (OWASP)

1. **Pre-hashing pepper**: the pepper is added to the password before the password hashing algorithm; the result is
   stored. The pepper should be a securely generated random value.
2. **Post-hashing pepper**: hash the password as usual, then hash the result with HMAC (for example HMAC-SHA256 or
   HMAC-SHA512) keyed with the pepper, and store that. The pepper is the HMAC key and is generated per the HMAC
   algorithm's key requirements.

If bcrypt must be used and the password is pre-hashed, OWASP's summary is
`bcrypt(base64(hmac-sha384(data:$password, key:$pepper)), $salt, $cost)` with the pepper stored outside the database.

## Where the pepper lives

- Not stored with the hash and not in the password database; OWASP says to keep it in a secrets vault or an HSM.
- Keep it out of source control and container images, and separate per environment.

## Rotation and loss

- A pepper cannot be changed without knowing each user's password, so replacing a compromised pepper means forcing
  every user it protected to reset their password (OWASP).
- Plan for this: store an identifier of the pepper version with each hash so both can be handled during a
  changeover.
- If the pepper leaks together with the database, you are back to the strength of the underlying hash.
- Losing the pepper locks out every user; back it up like any other critical secret.

## Verify

- [ ] A DB dump plus application code without the secret store cannot verify any password.
- [ ] Pepper backup and a reset-all-users runbook exist.

## Checked
2026-11-01. Confirmed against the OWASP Password Storage Cheat Sheet (Peppering section): shared pepper, separate
storage, vault or HSM, pre- and post-hashing strategies, change requires password resets, bcrypt summary. Removed:
the encrypt-the-hash construction and its batch rotation, the 72-byte and NUL-byte remarks, and the Argon2id
default (not in the fetched section). NIST SP 800-63B and SP 800-132 are listed as background only; no claim here
depends on them.
Method: documentation only; no commands were run.
