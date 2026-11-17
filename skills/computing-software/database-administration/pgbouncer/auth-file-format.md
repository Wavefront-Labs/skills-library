---
id: computing-software.database-administration.pgbouncer.auth-file-format
name: auth-file-format
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, auth-file, userlist, md5, scram]
level: practitioner
status: docs-checked
description: "Format of the auth_file (userlist.txt): quoted fields, plain, MD5 and SCRAM entries and their limitations."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write a correct auth_file.

Each line has at least two double-quoted fields: user name, then a plain-text password, an MD5 hash or a SCRAM secret. PgBouncer ignores the rest of the line. A double quote inside a value is escaped by doubling it.

```
"username1" "password"
"username2" "md5abcdef012342345"
"username2" "SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>"
```

The MD5 format is "md5" + md5(password + username); user admin with password 1234 gives `md545f2603610af569b6155c45067268c6b`.

The stored values serve two purposes: verifying incoming client passwords, and supplying the password for outgoing connections to a backend that wants password authentication (unless a password is in the database connection string).

Limitations:

- Plain text works for any backend method (plain, MD5 or SCRAM).
- MD5 hashes work only if the backend uses MD5 authentication (or those users have MD5 hashes).
- SCRAM secrets can log in to the server only if client authentication also uses SCRAM, the PgBouncer database definition has no user name, and the secrets are identical to the server's (same salt and iterations).

The file can be hand-written or generated; the source tree has `./etc/mkauth.py`, a sample script that builds it from pg_authid. Alternatively use auth_query to avoid maintaining the file. RELOAD re-reads auth_file.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
