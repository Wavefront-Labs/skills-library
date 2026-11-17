---
id: computing-software.email-administration.dovecot.static-passdb-and-userdb
name: static-passdb-and-userdb
category: computing-software
field: email-administration
product: dovecot
tags: [static-passdb, static-userdb, userdb-static-allow-all-users, proxy-setup, fixed-uid-gid]
level: practitioner
status: docs-checked
description: "Use static passdb and userdb for tests and proxies, with single uid and gid values, and handle LDA user verification."
sources:
  - https://doc.dovecot.org/main/core/config/auth/databases/static.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A static password database lets users log in with any username (the manual flags this as a danger). It is typically for testing, proxying and similar special setups. For the password, set either `password` in the passdb block or `nopassword = yes` in its `fields`; other passdb extra fields (such as `proxy = yes` and `host`) can also be returned. The userdb form is `userdb static { fields { uid = ... gid = ... home = <template> } }`. Settings variables are usable everywhere, so the result can be built from the login name.

A static user database suits installations with one UID and GID for every user and a home directory that follows a simple template. `home` is optional and other userdb extra fields can be returned. For the basic fixed fields a static userdb is not even needed: omit the userdb and set `mail_uid`, `mail_gid` and `mail_home` instead.

LDA caveat. Unless your MTA already verified the recipient, you want `dovecot-lda` to check that the user exists. LDA looks users up only in the userdb, and a static userdb has no list of users, so it falls back to doing a passdb lookup. This works with most passdbs; PAM is the main exception.

To skip that verification, add `userdb_static_allow_all_users = yes` to the userdb settings, which skips the passdb lookup. Use this only when the MTA validates recipients; without any check, delivery would not detect unknown users.

Do not use a static passdb as a real credential store. Because any username succeeds, restrict where it is reachable, for example behind a proxy that has already authenticated the user.

## Checked

2026-11-08. Read the Static database page in full. Added the password options and block syntax, named mail_uid, mail_gid and mail_home, and removed an unsourced claim about directories created for unknown users.

Method: documentation only; no commands were run.
