---
id: computing-software.systems-network-administration.headscale.upgrade-backup
name: upgrade-backup
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, backup, sqlite, postgresql, data-directory]
level: practitioner
status: docs-checked
description: "What to back up before a Headscale upgrade for standard, container and PostgreSQL installs: the config and data directories with the SQLite database."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up Headscale

The upgrade procedure stops Headscale before the backup is taken.

## Standard installation

Copy both directories to timestamped locations:

- configuration file `/etc/headscale/config.yaml` (the directory `/etc/headscale`)
- data directory `/var/lib/headscale`, which holds the SQLite database `/var/lib/headscale/db.sqlite`

```
TIMESTAMP=$(date +%Y%m%d%H%M%S)
cp -aR /etc/headscale /etc/headscale.backup-$TIMESTAMP
cp -aR /var/lib/headscale /var/lib/headscale.backup-$TIMESTAMP
```

## Container

Copy the single volume directory holding config, data and the SQLite database:

```
cp -aR /path/to/headscale /path/to/headscale.backup-$(date +%Y%m%d%H%M%S)
```

## PostgreSQL

Follow PostgreSQL's own Backup and Restore documentation.

## Gotchas

- Take the backup before every upgrade: Headscale applies database migrations during upgrades.

## Checked

2026-11-04. Confirmed against the Headscale upgrade page (Backup): standard installation paths, the cp commands for standard and container installs, and the PostgreSQL pointer. Removed unsourced claims about keys and policy in the data directory, PostgreSQL maintenance mode, and the stop-for-consistency rationale.
Method: documentation only; no commands were run.
