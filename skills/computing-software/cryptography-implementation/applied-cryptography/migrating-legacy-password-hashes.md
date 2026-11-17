---
id: computing-software.cryptography-implementation.applied-cryptography.migrating-legacy-password-hashes
name: migrating-legacy-password-hashes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, password-hashing, password-hash-migration, md5, sha1, argon2id, rehash-on-login, passlib, django]
level: practitioner
status: docs-checked
description: "Move legacy MD5, SHA-1 or unsalted hashes to Argon2id without resets: wrap all hashes now, upgrade on login, and expire dormant accounts."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#upgrading-legacy-hashes", "https://docs.djangoproject.com/en/stable/topics/auth/passwords/#password-upgrading", "https://passlib.readthedocs.io/en/stable/narr/context-tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating legacy password hashes

Waiting for users to log in leaves weak hashes in the database for years.
Do both: wrap everything now, then upgrade to a clean hash on login.

## Step 1: wrap every legacy hash immediately

```
new = argon2id(legacy_hash)            # legacy_hash = md5(salt+pw), sha1(pw), ...
store: scheme="argon2id(md5)", params, salt, new
```

Run as a batch job; afterwards no raw MD5/SHA-1 values remain at rest.
Verification: compute the legacy hash from the submitted password, then
verify against the Argon2id wrapper.

Caveat: a wrapped unsalted hash can be "shucked" (attacker tests leaked
MD5 lists against the outer layer), so step 2 still matters.

## Step 2: upgrade on successful login

```python
if scheme == "argon2id(md5)" and verify_wrapped(pw, row):
    row = {"scheme": "argon2id", "hash": ph.hash(pw)}
elif needs_rehash(row.hash):  # parameters weaker than current policy
    row.hash = ph.hash(pw)
```

Framework support:
- Django: list the new hasher first in `PASSWORD_HASHERS`; old ones remain
  for verification and are upgraded on login automatically (never remove
  entries users still depend on). Django docs show a "wrapped" password hasher
  (`PBKDF2WrappedMD5PasswordHasher`) for step 1.
- passlib: a `CryptContext` listing the new and old schemes with the old ones
  in `deprecated`, then `verify_and_update`.

## Step 3: handle dormant accounts

OWASP's first upgrade method: expire and delete the hashes of users who have
been inactive for an extended period and require them to reset their passwords.
It is secure but not user-friendly; warn support staff, since users may read
it as a breach. Choose the deadline yourself.

## Rules

- Store a scheme identifier with every hash; never guess from length.
- Constant-time comparison for legacy checks too.
- Do not log submitted passwords during migration debugging.

## Verify

- [ ] Zero raw legacy hashes at rest after the batch job.
- [ ] Login upgrades scheme; count of wrapped hashes falls over time.
- [ ] Deadline and reset flow documented.

## Checked
2026-11-01. Confirmed: Django password-upgrading docs (`PASSWORD_HASHERS` order, automatic upgrade at login,
wrapped hasher for MD5, `PBKDF2WrappedMD5PasswordHasher`); passlib CryptContext tutorial (`deprecated`,
`verify_and_update`); OWASP Password Storage Cheat Sheet (upgrade on login, expire inactive users' hashes, password
shucking risk of pre-hashing). Removed: the 12-month figure, `check_needs_rehash`, the wrapped-SHA1 class name.
Method: documentation only; no commands were run.
