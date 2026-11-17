---
id: computing-software.database-administration.pgbouncer.forced-user-and-connect-query
name: forced-user-and-connect-query
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, forced-user, connect-query, databases-section, pooling]
level: advanced
status: docs-checked
description: "Using user= in a database entry to force one backend user, with connect_query and effects on pool counts and min_pool_size."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route all clients to one backend role and prepare each server session.

Setting `user=` in a [databases] entry makes PgBouncer log in to the destination as that user regardless of the client user, so there is only one pool for that database. Without it, PgBouncer logs in as the client user, giving one pool per user. SHOW DATABASES shows this as `force_user`.

```
[databases]
forcedb = host=localhost port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO
```

Details:

- `password=` in the entry wins; otherwise the auth_file password for that user is used. auth_query-style discovery is not supported for it.
- `auth_type = any` requires every database to be configured to log in as a specific user.
- `min_pool_size` is enforced for pools whose entry has a user key (forced user) even with no clients connected.
- SCRAM secrets from auth_file cannot be used for server login when the database definition names a user.
- `max_user_connections` counts the forced server user.

`connect_query` runs after each server connection is established and before any client can use it. Errors from it are logged and otherwise ignored.

Related per-database parameters sent to the server: `client_encoding`, `datestyle`, `timezone`.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a connect_query example whose quoting the docs do not show.

Method: documentation only; no commands were run.
