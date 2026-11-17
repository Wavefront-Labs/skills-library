---
id: computing-software.database-administration.cloudnative-pg.pg-hba-rules-order-and-defaults
name: pg-hba-rules-order-and-defaults
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pg-hba, authentication, hostssl, scram-sha-256, streaming-replica, access-control]
level: practitioner
status: docs-checked
description: "Add custom pg_hba rules to a CloudNativePG cluster knowing the generated file order of fixed rules, your rules, LDAP and the default scram-sha-256 or md5 rule."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add rules as list items in `.spec.postgresql.pg_hba`. Because PostgreSQL uses the first matching rule, the generated file has four parts: fixed rules, your rules, optional LDAP rule, default rules.

```text
local all all peer

hostssl postgres streaming_replica all cert map=cnpg_streaming_replica
hostssl replication streaming_replica all cert map=cnpg_streaming_replica
hostssl all cnpg_pooler_pgbouncer all cert map=cnpg_pooler_pgbouncer

<user defined rules>
<user defined LDAP>

host all all all scram-sha-256 # (or md5 for PostgreSQL version <= 13)
```

Example granting the `app` user access to the `app` database over TLS from a pod network:

```yaml
  postgresql:
    pg_hba:
      - hostssl app app 10.244.0.0/16 md5
```

The default authentication method is `scram-sha-256` from PostgreSQL 14, when `password_encryption` defaults to it; PostgreSQL 13 and older use `md5`. The fixed rules give local `peer` access, certificate access for `streaming_replica` and certificate access for the PgBouncer pooler user. Your rules sit before the final `host all all all` default rule. Instances reload the configuration immediately after a change to the `postgresql` section.

## Checked

2026-11-04. Trimmed claims the page does not state. pg_hba composition, fixed rules and PostgreSQL 14 scram default confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
