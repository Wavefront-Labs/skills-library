---
id: computing-software.database-administration.pgbouncer.auth-type-methods
name: auth-type-methods
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, auth-type, md5, scram-sha-256, authentication]
level: practitioner
status: docs-checked
description: "Every auth_type value (cert, md5, scram-sha-256, plain, trust, any, hba, ldap, pam) and what each requires."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the client authentication method.

PgBouncer authenticates clients itself using its own user database. `auth_type` values:

- `md5` (default): MD5-based password check. auth_file may hold MD5 or plain-text passwords. If a user has a SCRAM secret, SCRAM is used automatically instead.
- `scram-sha-256`: auth_file must contain SCRAM secrets or plain-text passwords.
- `plain`: clear-text password over the wire. Deprecated.
- `trust`: no authentication, but the user name must still exist in auth_file.
- `any`: like trust but the user name is ignored. Requires every database to be configured to log in as a specific user. The console database lets any user log in as admin.
- `cert`: client must use TLS with a valid client certificate; the user name is the certificate CommonName.
- `hba`: the real method is loaded from auth_hba_file, allowing different methods per access path (for example peer over Unix socket, TLS required over TCP).
- `ldap`: authenticate against an LDAP server as in PostgreSQL; options come from auth_ldap_options or the HBA file.
- `pam`: PAM validates users, auth_file is ignored. Not compatible with databases using auth_user. The PAM service name is pgbouncer. pam is not supported in the HBA file.

Most types need either auth_file or auth_user set, otherwise no users are defined. ldap and pam require a build with those libraries.

```
auth_type = scram-sha-256
auth_file = /path/to/userlist.txt
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
