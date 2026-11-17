---
id: computing-software.database-administration.postgresql.debian-pg-upgradecluster-and-pg-lsclusters
name: debian-pg-upgradecluster-and-pg-lsclusters
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-upgrade, major-version-upgrade, pg-upgradecluster, pg-lsclusters, debian, ubuntu, postgresql-common]
level: practitioner
status: docs-checked
description: "Manage clusters on Debian and Ubuntu with postgresql-common: list them with pg_lsclusters and do major upgrades with pg_upgradecluster (dump, upgrade, link, clone)."
sources:
  - https://manpages.debian.org/testing/postgresql-common/pg_upgradecluster.1.en.html
  - https://manpages.debian.org/testing/postgresql-common/pg_lsclusters.1.en.html
  - https://www.postgresql.org/docs/current/pgupgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debian/Ubuntu clusters: pg_lsclusters and pg_upgradecluster

Debian's `postgresql-common` wraps PostgreSQL so several versions and clusters coexist.
The upgraded cluster's data directory defaults to `/var/lib/postgresql/<newversion>/<name>`.

## Everyday commands
```bash
pg_lsclusters                  # status of every cluster: online or down
pg_lsclusters -j               # JSON output (needs libjson-perl)
pg_lsclusters -s               # include start.conf information in the status column
pg_lsclusters 17 main          # only that version and cluster
```
Start, stop and creation commands (`pg_ctlcluster`, `pg_createcluster`, `pg_dropcluster`) come from the same package:
read their man pages before use; the old cluster is dropped with `pg_dropcluster` once verified.

## Major upgrade with pg_upgradecluster
```bash
sudo pg_upgradecluster --check 16 main              # are all packages for the upgrade installed?
sudo pg_upgradecluster -m upgrade --link 16 main    # pg_upgrade underneath, hard links
# -m dump (the default): pg_dumpall, slow but safe
# -m clone: file cloning (reflinks) via pg_upgrade --clone
pg_lsclusters
```
`-m link` and `-m clone` are shorthands for `-m upgrade --link` and `-m upgrade --clone`; `-v` picks the target
version (default: latest available). What it does for you: copies the old config files and adjusts them for the new
version, moves the old cluster to a previously unused port so the upgraded cluster takes the original port
(`--keep-port` disables the swap), and does not remove the old cluster, which is set to "manual" startup.
The new cluster is started if the old one was running (`--[no-]start`). It does not automate index rebuilds or
`ALTER COLLATION ... REFRESH VERSION` when libc/libicu collation order changes across an OS upgrade.

`pg_upgrade --check` is the underlying dry run; always run the new server's binary, with
`--old-bindir`, `--new-bindir`, `--old-datadir`, `--new-datadir` and, on Debian layouts, `--old-options` /
`--new-options` pointing at the config files. If `--check` was used the old cluster is unmodified.

## After the upgrade
```bash
sudo -u postgres psql -c 'select version()'
```
The docs say to verify the new cluster, then remove the old one with `pg_dropcluster`. With link mode do not start the old
cluster once the new one has run. Run any script files pg_upgrade generated (`psql --username=postgres --file=script.sql postgres`)
and regenerate statistics as pg_upgrade instructs (`vacuumdb --all --analyze-in-stages --missing-stats-only`, then `vacuumdb --all --analyze-only`).

## Gotchas
- Extensions need the same packages for the new version installed first; `--check` reports missing packages and
  `--force-packages` proceeds anyway (avoid).
- Extensions such as PostGIS can need hook scripts: executable files in `/etc/postgresql-common/pg_upgradecluster.d/`
  are called with `<old version> <cluster name> <new version> <phase>` (`init`, `finish`); a failing script aborts the upgrade.
- If the upgrade fails the newly created cluster is removed unless you pass `--keep-on-error`.
- Applications pointing at the old cluster's port break after the port swap.

## Verify
`pg_lsclusters` shows the new version online on the original port; applications connect,
and `SELECT extversion FROM pg_extension` shows expected versions.

## Checked

2026-10-31. Confirmed against the pg_upgradecluster and pg_lsclusters man pages (postgresql-common 293) and the pg_upgrade page: methods and defaults, `--check`, `--keep-port`, `--[no-]start`, `--keep-on-error`, `--force-packages`, hook scripts, collation caveat, default data directory, pg_lsclusters options and statuses, post-upgrade vacuumdb commands. Removed unconfirmed: config and unit paths, pg_ctlcluster/pg_createcluster/pg_dropcluster option examples, automatic empty cluster creation, port numbers, `update_extensions.sql`, apt repository advice.

Method: documentation only; no commands were run.
