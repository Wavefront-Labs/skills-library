---
id: computing-software.data-engineering.metabase.upgrading
name: upgrading
category: computing-software
field: data-engineering
product: metabase
tags: [upgrading, migrate-down, downgrade, rollback, docker-tags, cluster-upgrade]
level: practitioner
status: docs-checked
description: "Upgrade self-hosted Metabase safely: backup first, Docker and JAR steps, pre-40 upgrade path, migrate down rollback, cluster rules and Cloud behaviour."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/upgrading-metabase
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Always back up the application database first.

Docker: stop the container, pull the new image with a specific tag rather than `latest` (`metabase/metabase` or `metabase/metabase-enterprise`), start a new container. Migrations run on startup.

JAR: `sudo systemctl stop metabase.service`, replace the JAR, `sudo systemctl restart metabase.service`. Pro/Enterprise JAR: `https://downloads.metabase.com/enterprise/latest/metabase.jar`.

Upgrade path: versions older than 40 must go one release at a time to the latest 40.x, then jump to current (1.38.X, 1.39.X, 1.40.X, latest). Between majors use the latest point release of the target major.

Rollback: preferred is restoring the pre-upgrade application database backup. Alternatively `migrate down` undoes schema changes and keeps later content, and must be run with the higher-version JAR after setting `MB_DB_*`:
`java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar migrate down`
On Docker pass `"migrate down"` in quotes. Without a downgrade, Metabase may refuse to start after a major rollback.

Clusters: scale to one node before a major upgrade; upgrading several nodes at once can break the app. Do not let the orchestrator kill Metabase mid-migration, or the application database may corrupt and need a restore.

Version format is major.minor.point (54.1 to 54.2 is minor). Cloud upgrades are automatic, except instances using the modular embedding SDK, which are pinned and must ask support.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Upgrading Metabase: backup first, Docker and JAR steps, pre-40 upgrade path, migrate down guidance and Docker quoting, cluster single-node rule, migration-kill warning, version format, Cloud behaviour and modular embedding SDK pinning. The enterprise JAR URL is linked from the page by name and was fetched with HTTP 200. Nothing removed.
Method: documentation only; no commands were run.
