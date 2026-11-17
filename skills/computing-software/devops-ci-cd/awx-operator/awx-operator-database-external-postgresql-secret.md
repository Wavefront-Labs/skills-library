---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-database-external-postgresql-secret
name: awx-operator-database-external-postgresql-secret
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, postgres, external-database, sslmode, target-session-attrs, postgres-configuration-secret]
level: advanced
status: docs-checked
description: "Point AWX at an external PostgreSQL through a postgres-configuration Secret, including sslmode, target_session_attrs and password restrictions."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/database-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator database external postgresql secret

Only the default PostgreSQL version (15 in current operators, per `supported_pg_version`) has coverage; newer versions will likely work but only as an external database.

Create a Secret and reference it as `postgres_configuration_secret` in the spec:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <resourcename>-postgres-configuration
stringData:
  host: <external ip or url resolvable by the cluster>
  port: <external port, usually 5432>
  database: <database name>
  username: <username>
  password: <password>
  sslmode: prefer
  target_session_attrs: read-write
  type: unmanaged
type: Opaque
```

- The password must not contain single or double quotes or backslashes, to avoid problems during deployment, backup or restore.
- `sslmode` is valid for external databases only: `prefer`, `disable`, `allow`, `require`, `verify-ca`, `verify-full`.
- `target_session_attrs` matters only for clustered external databases: `any` (default), `read-write`, `read-only`, `primary`, `standby`, `prefer-standby`; only `read-write` and `primary` really make sense for AWX.
- To set a specific username, password, port or database but keep the database operator-managed, add `type: managed` to the secret.

## Checked

2026-11-04. Confirmed against the AWX Operator "Database Configuration" page (PostgreSQL Version and External PostgreSQL Service sections): version coverage, Secret fields, password restriction, `sslmode` and `target_session_attrs` values, and `type: managed`. Nothing removed.
Method: documentation only; no commands were run.
