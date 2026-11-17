---
id: computing-software.email-administration.mail-server-administration.dovecot-passdb-userdb
name: dovecot-passdb-userdb
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dovecot-passdb-userdb, dovecot-auth, passdb, userdb, passwd-file]
level: practitioner
status: docs-checked
description: "Configure a Dovecot passwd-file passdb and static userdb for virtual users and choose a password scheme."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/authentication/passwd_file/
  - https://doc.dovecot.org/2.3/configuration_manual/authentication/static_user_database/
  - https://doc.dovecot.org/2.3/configuration_manual/authentication/password_schemes/
  - https://doc.dovecot.org/2.3/admin_manual/debugging/debugging_authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dovecot passdb userdb

**Goal:** authenticate users and tell Dovecot where their mail lives (doc.dovecot.org authentication).
## Steps
1. `passdb { driver = passwd-file  args = scheme=ARGON2ID /etc/dovecot/users }` (`scheme=` sets the passdb default scheme, CRYPT if omitted; ARGON2ID needs libsodium, otherwise use `SHA512-CRYPT`).
2. `userdb { driver = static  args = uid=vmail gid=vmail home=/var/vmail/%d/%n }` (static userdb has no user list, so existence checks fall back to a passdb lookup).
3. Generate a hash: `doveadm pw -s SHA512-CRYPT`.
4. Reload: `doveadm reload`.
## Failure modes
- Plaintext schemes in the file; always hash.
- Block syntax above is Dovecot 2.3; 2.4 changed the configuration syntax, so compare with `doveconf -n` after upgrading.
## Verify
- `doveadm auth test alice@example.com` and `doveadm user alice@example.com` show the expected uid and home.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 docs: passwd-file page (scheme= arg, default CRYPT), static userdb page (args uid, gid, home), password schemes page (ARGON2ID needs libsodium, `doveadm pw -s SHA512-CRYPT`), debugging authentication page (`doveadm auth test`, `doveadm user`) and the `doveadm reload` entry of the doveadm API reference. Removed the unsourced home-directory permission failure mode.

Method: documentation only; no commands were run.
