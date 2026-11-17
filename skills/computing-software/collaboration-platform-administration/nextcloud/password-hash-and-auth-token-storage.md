---
id: computing-software.collaboration-platform-administration.nextcloud.password-hash-and-auth-token-storage
name: password-hash-and-auth-token-storage
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [hardening, argon2id, authentication-token, instance-secret, password-hash]
level: advanced
status: draft
description: "Understand how Nextcloud stores account password hashes and hashed authentication tokens, and what a leak of tokens, the instance secret or hashes allows."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/installation/harden_server.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: know what is stored, so you can judge the impact of a database or config leak.

Account passwords (built-in database user backend): a salted one-way hash. Nextcloud prefers Argon2id when PHP supports it, with Argon2i and bcrypt as fallbacks. Algorithm, salt and cost are inside the stored hash, and old hashes are upgraded automatically after a successful verification. With an external backend such as LDAP, that backend controls storage and verification.

Authentication tokens: after login the client presents a token (via session cookie, app password or bearer token). The plaintext token is not stored; the database holds a SHA-512 hash derived from the token and the instance-specific `secret` in `config.php`. Treat tokens like passwords: never log them, put them in URLs, or persist them outside the client.

Consequences of leakage:
- Someone with a valid token can authenticate as that user, within the token's scope, expiry, type and server-side validity checks.
- Someone with the token, the instance `secret` and the matching database record can decrypt a login password stored in that record (see stored-login-password-setting).
- A leaked account-password hash does not reveal the password directly, but allows offline guessing attacks.


Check: confirm Argon2 is available in your PHP (see php-modules-required-and-recommended), since existing Argon2 hashes need it to verify.
