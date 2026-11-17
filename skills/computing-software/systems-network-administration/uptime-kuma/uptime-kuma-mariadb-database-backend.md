---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-mariadb-database-backend
name: uptime-kuma-mariadb-database-backend
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [mariadb, uptime-kuma-database, db-type, embedded-mariadb, docker-secrets, db-password-file, sqlite]
level: advanced
status: docs-checked
description: "Point Uptime Kuma 2 at MariaDB with UPTIME_KUMA_DB_* variables, docker secrets via _FILE variants, or embedded MariaDB."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Environment-Variables", "https://github.com/louislam/uptime-kuma/wiki/Docker-Tags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma with MariaDB

Default storage is SQLite in the data directory. Version 2 can use MariaDB instead:

| Variable | Since | Meaning |
|---|---|---|
| `UPTIME_KUMA_DB_TYPE` | 2.0.0 | `sqlite` or `mariadb` |
| `UPTIME_KUMA_DB_HOSTNAME` / `UPTIME_KUMA_DB_PORT` | 2.0.0 | host and port (`3306`) |
| `UPTIME_KUMA_DB_SOCKET` | 2.1.0 | Unix socket; hostname and port are then ignored |
| `UPTIME_KUMA_DB_NAME`, `_USERNAME`, `_PASSWORD` | 2.0.0 | credentials |
| `UPTIME_KUMA_DB_POOL_MAX_CONNECTIONS` | 2.1.0 | pool size, default 10 |
| `UPTIME_KUMA_DB_SSL` | 2.1.0 | `true`/`false`, default false |
| `UPTIME_KUMA_DB_CA` | 2.1.0 | PEM CA certificate content for SSL |

For Docker secrets, `UPTIME_KUMA_DB_PASSWORD_FILE`, `UPTIME_KUMA_DB_USERNAME_FILE` and `UPTIME_KUMA_DB_CA_FILE` read the value from a file path instead.

```yaml
environment:
  UPTIME_KUMA_DB_TYPE: mariadb
  UPTIME_KUMA_DB_HOSTNAME: mariadb
  UPTIME_KUMA_DB_NAME: kuma
  UPTIME_KUMA_DB_USERNAME: kuma
  UPTIME_KUMA_DB_PASSWORD_FILE: /run/secrets/kuma_db_password
```

Embedded MariaDB ships only in the full image (`UPTIME_KUMA_ENABLE_EMBEDDED_MARIADB=1`); the slim image requires an external MariaDB/MySQL. For SQLite, `UPTIME_KUMA_SQLITE_SINGLE_CONNECTION` (2.3.2, default true) can be set false for multiple connections, which may raise `SQLITE_BUSY: database is locked`.

The migration guide has an FAQ on moving an existing SQLite database to MariaDB; read it before attempting that.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Environment Variables page (MariaDB variables, since versions, _FILE variants, embedded MariaDB flag), Docker Tags page (full versus slim) and Migration From v1 To v2 FAQ. Removed: The generic verify line.

Method: documentation only; no commands were run.
