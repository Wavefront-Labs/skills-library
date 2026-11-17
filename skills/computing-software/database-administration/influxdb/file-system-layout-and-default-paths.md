---
id: computing-software.database-administration.influxdb.file-system-layout-and-default-paths
name: file-system-layout-and-default-paths
category: computing-software
field: database-administration
product: influxdb
tags: [file-system, engine-path, bolt-path, sqlite-path, configs-path, docker]
level: intro
status: docs-checked
description: "Where OSS stores data by install method: engine, bolt, SQLite and configs paths for standalone, packages and the Docker image, and what each holds."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/file-system-layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

What each path holds:
- Engine path: `data` (TSM files), `wal` (write-ahead log) and `replicationq` (replication queues). Option `engine-path`.
- Bolt path (`bolt-path`): BoltDB key-value store for users, dashboards, tasks.
- SQLite path (`sqlite-path`): notebooks and annotations.
- Configs path: `influx` CLI connection configs; use `--configs-path` to change.

Defaults:

| Install | Engine | Configs path |
|---|---|---|
| macOS / Linux standalone | `~/.influxdbv2/engine/` | `~/.influxdbv2/configs` |
| Linux .deb/.rpm package | `/var/lib/influxdb/engine/` | `/var/lib/influxdb/configs` |
| Windows | `%USERPROFILE%\.influxdbv2\engine\` | `%USERPROFILE%\.influxdbv2\configs` |
| Docker Hub image | `/var/lib/influxdb2/engine/` | `/etc/influxdb2/configs`, or `/etc/influxdb2/influx-configs` after automated `setup` mode or `influx setup` in the container |
| Quay.io image | `/root/.influxdbv2/engine/` | `/root/.influxdbv2/configs` |

The package layout keeps `influxd.bolt`, `influxd.sqlite` and `configs` beside the engine in `/var/lib/influxdb/`, with the default `influxd` config file at `/etc/influxdb/config.toml`. The Docker Hub image uses `/var/lib/influxdb2` instead of `/var/lib/influxdb` so 1.x and 2.x volumes can be mounted separately during upgrade.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): path purposes, `engine-path`, `bolt-path`, `sqlite-path` and `--configs-path`, and the default paths for macOS, Linux standalone and package, Windows, Docker Hub, Quay.io. Corrected the Docker configs path and the config column, which the previous table mixed.
Method: documentation only; no commands were run.
