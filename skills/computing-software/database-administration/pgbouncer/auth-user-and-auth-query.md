---
id: computing-software.database-administration.pgbouncer.auth-user-and-auth-query
name: auth-user-and-auth-query
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, auth-user, auth-query, pg-authid, security-definer]
level: advanced
status: docs-checked
description: "Look up passwords from the database with auth_user and auth_query, including the default query and a SECURITY DEFINER function."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate users that are not in auth_file by querying PostgreSQL.

If `auth_user` is set, any user missing from auth_file is looked up with `auth_query` against the database, connecting as auth_user. auth_user's own password comes from auth_file (not needed if it requires none). `auth_query` and `auth_user` can be overridden per [databases] entry (the whole SQL statement must then be in single quotes), as can `auth_dbname`, which picks the [databases] entry used for authentication.

Default auth_query:

```
SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END FROM pg_authid WHERE rolname=$1 AND rolcanlogin
```

The query runs inside the target database, so a function must be installed in each database. It must return two columns: user name and password (encrypted or hashed). No rows, or a null user, means the user does not exist; a null password means the user exists but no offered password is accepted.

Direct access to pg_authid needs admin rights. Prefer a non-superuser calling a SECURITY DEFINER function with a secure search_path:

```
CREATE OR REPLACE FUNCTION pgbouncer.user_lookup(in i_username text, out uname text, out phash text)
RETURNS record AS $$
BEGIN
  SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END
  FROM pg_authid WHERE rolname=i_username AND rolcanlogin INTO uname, phash;
  RETURN;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog, pg_temp;
```

Revoke execute from public and grant it to the auth user. Dynamic password discovery is not supported for the per-database password key.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
