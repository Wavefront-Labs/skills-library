---
id: computing-software.database-administration.cloudnative-pg.pooler-authentication-auth-query-and-custom-secrets
name: pooler-authentication-auth-query-and-custom-secrets
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pooler, pgbouncer, auth-query, auth-user, cnpg-pooler-pgbouncer, tls, pg-ident]
level: advanced
status: docs-checked
description: "Understand built-in PgBouncer authentication (cnpg_pooler_pgbouncer, user_search function), what changes with your own certificate secrets, and how to override auth_user."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/connection_pooling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the pooler reuses the cluster certificates and uses TLS client certificates to run `auth_query` for password authentication. The built-in integration:

- creates the user `cnpg_pooler_pgbouncer`;
- creates a lookup function in the `postgres` database and grants it `EXECUTE`;
- issues a TLS certificate for that user;
- sets `cnpg_pooler_pgbouncer` as `auth_user` and `postgres` as `auth_dbname`;
- removes all of it when no pooler is associated with the cluster.

The function, created by the instance manager as `postgres` against the `postgres` database, is pinned to a safe search path:

```sql
CREATE OR REPLACE FUNCTION public.user_search(uname TEXT)
  RETURNS TABLE (usename name, passwd text)
  LANGUAGE sql SECURITY DEFINER
  SET search_path = pg_catalog, pg_temp AS
  'SELECT usename, passwd FROM pg_catalog.pg_shadow WHERE usename=$1;';

REVOKE ALL ON FUNCTION public.user_search(text)
  FROM public;

GRANT EXECUTE ON FUNCTION public.user_search(text)
  TO cnpg_pooler_pgbouncer;
```

Clusters created by older versions are migrated to the pinned `search_path` on upgrade.

Supplying your own certificate secrets (Basic Auth, TLS or Opaque with `tls.crt` and `tls.key`) disables this integration, and you own authentication. To change the authenticating role set `auth_user`; with certificates, the built-in `pg_hba` and `pg_ident` rules match only the literal `cnpg_pooler_pgbouncer`, so add a mapping on the `Cluster`:

```yaml
postgresql:
  pg_ident:
    - poolermap pooler-client-cn pgbouncer
  pg_hba:
    - hostssl all pgbouncer all cert map=poolermap
```

For basic-auth secrets, the secret password must be the real password of the overridden `auth_user` role.

## Checked

2026-11-04. Built-in integration steps, SQL statements and auth_user override with pg_ident mapping confirmed on the Connection pooling page.

Method: documentation only; no commands were run.
