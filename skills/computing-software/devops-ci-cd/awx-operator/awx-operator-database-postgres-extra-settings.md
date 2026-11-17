---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-database-postgres-extra-settings
name: awx-operator-database-postgres-extra-settings
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, postgresql-conf, postgres-extra-settings, max-connections, deprecated, tuning]
level: practitioner
status: docs-checked
description: "Set postgresql.conf values with postgres_extra_settings (replacing the deprecated postgres_extra_args) and verify them."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/database-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator database postgres extra settings

`postgres_extra_settings` writes entries to `postgresql.conf` for the managed database. It takes an array of objects with `setting` and `value`; `postgres_extra_args` is deprecated, should no longer be used and will be removed in a future version of the operator. Default for `postgres_extra_settings`: `[]`.

```yaml
spec:
  postgres_extra_settings:
    - setting: max_connections
      value: "499"
    - setting: ssl_ciphers
      value: "HIGH:!aNULL:!MD5"
```

Settings the docs list as common (with example values): `max_connections` ("200"), `ssl_ciphers`, `shared_buffers` ("256MB"), `effective_cache_size` ("1GB"), `work_mem` ("4MB"), `maintenance_work_mem` ("64MB"), `checkpoint_completion_target` ("0.9"), `wal_buffers` ("16MB").

Notes:
- Changes require a PostgreSQL pod restart.
- Some settings need specific PostgreSQL versions or extra configuration; test in non-production first.
- Quote string values; numbers may be strings or numbers; booleans go as strings ("on"/"off" or "true"/"false").

Verify by connecting with `kubectl exec -it <postgres-pod-name> -n <namespace> -- psql` and running `SELECT name, setting FROM pg_settings;`. For the full list of parameters, see the PostgreSQL documentation.

## Checked

2026-11-04. Confirmed against the AWX Operator "Database Configuration" page (PostgreSQL Extra Settings section): parameter format, deprecation notice, the eight common settings and example values, the notes, and the verification commands. Removed a duplicated paragraph and the invented "runtime-config" page reference.
Method: documentation only; no commands were run.
