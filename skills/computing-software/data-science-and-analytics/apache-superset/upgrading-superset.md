---
id: computing-software.data-science-and-analytics.apache-superset.upgrading-superset
name: upgrading-superset
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [upgrading, db-upgrade, superset-init, backup, staging]
level: practitioner
status: docs-checked
description: "Upgrade a Superset instance safely: back up the metadata database, rehearse on staging, then apply the Docker or pip steps, db upgrade and init."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/upgrading-superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move to a newer Superset release without data loss.

Before you start:
- Back up the metadata database. Upgrading should not delete charts and dashboards, but the docs recommend a backup anyway.
- Rehearse in a staging environment, and upgrade production last, at off-peak usage.
- Read UPDATING.md for breaking changes (configuration, API, database migrations, deprecated features).

Docker Compose installs:

```bash
docker compose down
git pull origin master
docker compose up
```

Changed Docker images are pulled automatically on `up`.

Native (pip) installs:

```bash
pip install apache_superset --upgrade
```

Then migrate the metadata database:

```bash
superset db upgrade
superset init
```

## Checked

2026-11-08: read upgrading-superset.mdx in full. Removed claims not on the page: pinned-tag advice, what `superset init` overwrites, multi-process ordering, cache clearing and smoke-test advice.
Method: documentation only; no commands were run.
