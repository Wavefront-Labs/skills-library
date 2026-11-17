---
id: computing-software.database-administration.cloudnative-pg.initdb-bootstrap-app-database-and-options
name: initdb-bootstrap-app-database-and-options
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [initdb, bootstrap, app-database, locale, data-checksums, encoding, basic-auth]
level: practitioner
status: docs-checked
description: "Create an empty cluster with the initdb stanza: app database and owner, basic-auth Secret, and typed options for locale, ICU, encoding, WAL segment size and data checksums."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/bootstrap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-example-initdb
spec:
  instances: 3

  bootstrap:
    initdb:
      database: app
      owner: app
      secret:
        name: app-secret

  storage:
    size: 1Gi
```

This runs `initdb`, creates an unprivileged user `app`, sets its password from `app-secret`, and creates database `app` owned by it. If you omit names, a defaulting webhook creates database `app` with a same-named owner and generates random passwords for both superuser and application user. The Secret must be `kubernetes.io/basic-auth` and its `username` must equal the `owner` (or `postgres` for the superuser Secret). The operator itself uses the superuser, not the application user.

Typed options that map straight to `initdb` flags: `builtinLocale` (needs `localeProvider: builtin`, PostgreSQL 17+), `dataChecksums`, `encoding` (default `UTF8`), `icuLocale` (PG 15+, needs provider `icu`), `icuRules` (PG 16+), `locale`, `localeCollate` and `localeCType` (default `C`), `localeProvider` (PG 15+), `walSegmentSize` (PostgreSQL default 16 MB).

`dataChecksums: true` passes `--data-checksums` before PostgreSQL 18; from 18, where checksums are default, `false` passes `--no-data-checksums`. Locale options are passed through unchecked, so you must verify bootstrap succeeds. Other `lc_*` categories go in PostgreSQL parameters. The older `options` array is deprecated because flags such as `--auth` or `-d` can break the operator.

## Checked

2026-11-04. initdb example, secret requirements, option list and dataChecksums semantics confirmed on the Bootstrap page; the legacy options array is noted there as deprecated.

Method: documentation only; no commands were run.
