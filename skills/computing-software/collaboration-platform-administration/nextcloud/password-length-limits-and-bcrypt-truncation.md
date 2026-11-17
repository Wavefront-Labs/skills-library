---
id: computing-software.collaboration-platform-administration.nextcloud.password-length-limits-and-bcrypt-truncation
name: password-length-limits-and-bcrypt-truncation
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [password-length, 469-bytes, bcrypt, argon2, multibyte]
level: advanced
status: docs-checked
description: "Know that Nextcloud accepts passwords up to 469 bytes, why multibyte characters hit it sooner, the 214 byte token overhead threshold and bcrypt 72 byte truncation."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/installation/harden_server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set realistic password length expectations when writing a policy.

Limit: Nextcloud accepts account passwords up to 469 bytes through its standard account-creation, password-change and password-reset interfaces. It is measured in bytes, so emoji or non-Latin characters reach it with fewer than 469 characters.

Two implementation details do not change that maximum but matter for policy:

Token encryption performance. With `auth.storeCryptedPassword` on and a password longer than 214 bytes, Nextcloud uses a larger RSA key for authentication-token records. That raises token-generation overhead but does not reject passwords of 215 to 469 bytes. If you expect very long or one-time passwords, consider turning the setting off, accepting the functional effects (see stored-login-password-setting).

Algorithmic truncation. Nextcloud prefers Argon2id, with Argon2i and bcrypt as fallbacks. Bcrypt considers only the first 72 bytes of its input. So whenever bcrypt is in use, characters after byte 72 do not contribute to the hash. Make sure Argon2 is available in PHP (the `sodium` module on older PHP, see php-modules-required-and-recommended) so long passwords are fully used.

External user backends such as LDAP may impose their own requirements.

Configure minimum length and complexity with the Password Policy app (see password-policy-options).

Check: confirm which hashing algorithm your PHP supports before promoting passphrases longer than 72 bytes.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/installation/harden_server.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
