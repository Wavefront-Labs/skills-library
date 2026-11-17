---
id: computing-software.messaging-and-integration.debezium.postgresql-replication-user-and-permissions
name: postgresql-replication-user-and-permissions
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, replication-user, privileges, security]
level: practitioner
status: docs-checked
description: "Create a least-privilege PostgreSQL role with REPLICATION and LOGIN for Debezium instead of using a superuser."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only a user with the `REPLICATION` attribute can read logical decoding streams. Superusers have it by default, but the guide says not to give the Debezium user elevated privileges. Create a dedicated role with minimum rights.

```sql
CREATE ROLE <name> REPLICATION LOGIN;
CREATE USER replication_user WITH REPLICATION IN ROLE cloudsqlsuperuser LOGIN PASSWORD 'secret';
ALTER USER existing_user WITH REPLICATION;
```

The second form is the documented Cloud SQL variant; run these as the `postgres` user or a member of the `cloudsqlsuperuser` group. The first form defines a role that you then grant to the connector user.

Privileges the connector needs depend on how publications are handled:

- `REPLICATION` and `LOGIN` for streaming.
- `SELECT` on captured tables for snapshots (table owners have it automatically).
- `CREATE` on the database if the connector creates publications with `pgoutput`.
- Table ownership to add a table to a publication, which is why the docs describe a shared replication group role.

Also allow the connector host in `pg_hba.conf` for replication connections. Replication is only permitted for a configured number of hosts.

Gotcha: the docs recommend creating publications manually; then the connector does not need `CREATE` on the database.

Check: connect as the new user from the connector host and confirm it has the `REPLICATION` attribute.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: REPLICATION and LOGIN, the CREATE ROLE and Cloud SQL forms, superuser warning, SELECT and CREATE privileges, ownership group, pg_hba.conf.
Removed or reworded: the 'safer pattern' opinion and the pg_roles query.
Method: documentation only; no commands were run.
