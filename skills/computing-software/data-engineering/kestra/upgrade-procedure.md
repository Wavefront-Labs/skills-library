---
id: computing-software.data-engineering.kestra.upgrade-procedure
name: upgrade-procedure
category: computing-software
field: data-engineering
product: kestra
tags: [upgrade, rollback, flyway, database-migrate, rolling-upgrade, helm]
level: advanced
status: docs-checked
description: "Upgrade Kestra safely: back up, read breaking changes, rolling upgrades per install type, minimising downtime, and manual database migration."
sources:
  - https://kestra.io/docs/administrator-guide/upgrades
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrade: back up the database (optional but recommended), read the release notes (including the Breaking Changes section at their end), perform a rolling upgrade of the components, apply any actions the release notes name (for example config changes). Test in non-production first. Downgrades are strongly discouraged; rollback means stop all components, restore a backup, restart the older version.

By install:

- Docker: change the image tag (the `-slim` suffix replaced `-no-plugins`).
- Compose: edit the tag, `docker compose up -d`.
- Standalone: download the binary, run `./kestra-VERSION server standalone`.
- Helm: `helm upgrade kestra kestra/kestra --set image.tag=v1.0.0`, or `-f values.yaml`.

Minimal downtime with separate components: stop executors and scheduler, then workers (graceful shutdown waits up to `kestra.server.terminationGracePeriod`, default `PT5M`), then webserver, indexer and controller. The webserver hosts the API, so stop and then start it immediately to avoid downtime; then restart the other components so executions can resume.

If a job does not finish, the Executor resubmits it to another worker unless `kestra.server.worker-task-restart-strategy` is `NEVER`. The Helm chart `terminationGracePeriodSeconds` defaults to 60 seconds.

Database migrations run automatically through Flyway at startup (history in `flyway_schema_history`). For large databases migrate manually before starting, with the same configuration:

```bash
kestra sys database migrate
```

Either keep the old version running, stop it, then run the command from the new version; or start the new version with `flyway.datasources.postgres.enabled=false` (replace `postgres` with your database type).

## Checked

2026-11-04. Confirmed against "Upgrade Kestra safely with rolling updates and rollback strategies" (administrator-guide/upgrades): upgrade and rollback steps, downgrade warning, per-install commands, -slim tag rename, shutdown order, terminationGracePeriod default, worker-task-restart-strategy NEVER, Helm terminationGracePeriodSeconds default 60, Flyway and flyway_schema_history, manual migrate command and both approaches. Reworded: backup is optional but recommended, and the webserver restart advice now follows the page.
Method: documentation only; no commands were run.
