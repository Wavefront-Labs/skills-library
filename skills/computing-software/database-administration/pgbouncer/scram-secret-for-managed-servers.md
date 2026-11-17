---
id: computing-software.database-administration.pgbouncer.scram-secret-for-managed-servers
name: scram-secret-for-managed-servers
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, scram, rds, pg-authid, userlist, password]
level: sme
status: docs-checked
description: "Obtain a SCRAM secret for PgBouncer when a managed server blocks reading pg_authid, using psql --echo-hidden."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give PgBouncer a SCRAM secret that matches the server when you cannot read pg_authid.

If the backend uses SCRAM, PgBouncer can only log in when it knows either the user's plain-text password or the exact SCRAM secret. Some cloud providers (for example AWS RDS) block pg_authid even for the most privileged user (`select * from pg_authid;` returns `permission denied for table pg_authid`), so an existing secret cannot be fetched.

Workaround: generate a secret for an arbitrary password with a tool that prints it. psql can:

```
psql --echo-hidden <connection_string>
postgres=# \password <role_name>
Enter new password for user "<role_name>":
Enter it again:
********* QUERY **********
ALTER USER <role_name> PASSWORD 'SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>'
**************************
```

Copy the secret from the QUERY output into PgBouncer's userlist.txt. psql has already applied it to the server in this flow.

If you used a different tool, you must also set the same secret on the server yourself:

```
alter role <role_name> password '<scram_secret>';
```

Remember the SCRAM limitation: the secret works for server logins only when client auth is also SCRAM, the database entry has no user name, and salt and iterations are identical on both sides. PgBouncer's own `scram_iterations` setting (default 4096) controls iterations when it encrypts a password with SCRAM-SHA-256; higher is stronger but slower.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
