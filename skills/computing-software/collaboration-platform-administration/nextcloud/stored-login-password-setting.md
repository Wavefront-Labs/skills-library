---
id: computing-software.collaboration-platform-administration.nextcloud.stored-login-password-setting
name: stored-login-password-setting
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [auth-storecryptedpassword, token-password, external-storage, rsa, hardening]
level: advanced
status: draft
description: "Decide whether to keep auth.storeCryptedPassword on, what features need a recoverable login password, and how password changes affect tokens."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/installation/harden_server.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: weigh a hardening switch against the features that depend on it.

By default `auth.storeCryptedPassword` is enabled. When a login password is available while a token is created, Nextcloud stores a reversibly encrypted copy in that token's server-side record. This is separate from the one-way account-password hash.

How it is protected: each record has its own RSA key pair. The password is encrypted with the public key; the private key is encrypted with the authentication token together with the instance `secret`. So the token, the secret and the database record are together enough to decrypt it.

What uses the recoverable copy:
- connecting to external storage with login credentials
- autoconfiguring accounts in the Mail app
- periodically checking that the login credentials are still valid

If a token was created without a login password, its record has none, and it stays that way until Nextcloud receives the password at a later login or password update.

Effect on password changes: when a token holds a stored password, Nextcloud checks it against the user backend periodically, and rejects the token if invalid. A token without one is not checked, so changing a password directly in an external backend does not invalidate it. It stays valid until it expires, is otherwise invalidated, or the user is disabled.



Check: after disabling, test every feature listed above that you rely on.
