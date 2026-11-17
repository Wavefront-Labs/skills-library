---
id: computing-software.systems-network-administration.headscale.database-choice
name: database-choice
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, sqlite, postgres, wal, database]
level: practitioner
status: docs-checked
description: "Choose and tune Headscale's database: SQLite recommended, PostgreSQL in maintenance mode, WAL settings, GORM options, and database debug logging."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database choice

The FAQ recommends SQLite: simple, scales well for Headscale's use cases, and most development and testing happens on it. PostgreSQL is supported but in maintenance mode. No official PostgreSQL-to-SQLite migration tool exists (community tools are listed on the integration tools page). Database choice has little effect on performance.

```yaml
database:
  type: sqlite
  debug: false
  gorm:
    parameterized_queries: true
    skip_err_record_not_found: true
    slow_threshold: 1000
  sqlite:
    path: /var/lib/headscale/db.sqlite
    write_ahead_log: true
    wal_autocheckpoint: 1000
```

- `type`: `sqlite` or `postgres`; the example config discourages Postgres (legacy).
- `write_ahead_log: true` (WAL) is recommended for production.
- `wal_autocheckpoint: 1000`; set 0 to disable automatic checkpointing.
- `slow_threshold` is in milliseconds.
- `debug: true` enables database debug mode and requires `log.level` to be `debug` or `trace`.
- Postgres keys (commented out in the example): host, port, name, user, pass, max_open_conns, max_idle_conns, conn_max_idle_time_secs, ssl.

## Gotcha

Headscale applies database migrations during upgrades, and the upgrade guide highly recommends backing up the database first. In a standard installation the data directory `/var/lib/headscale` holds the SQLite database (upgrade-backup).

## Checked

2026-11-04. Confirmed against the Headscale FAQ (database recommendation, maintenance mode, migration tooling, performance), config-example.yaml (every key shown, WAL and GORM comments, Postgres keys) and the upgrade page (backup paths). Corrected the debug description and the backup gotcha.

Method: documentation only; no commands were run.
