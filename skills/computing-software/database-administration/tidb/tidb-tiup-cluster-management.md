---
id: computing-software.database-administration.tidb.tidb-tiup-cluster-management
name: tidb-tiup-cluster-management
category: computing-software
field: database-administration
product: tidb
tags: [tidb, tiup, tiup-playground, tiup-cluster, package-manager, install, mirror, components]
level: intro
status: docs-checked
description: "Install and use TiUP, the TiDB component manager: one-line install, playground, cluster deployment, update, list, clean and mirror commands."
sources: ["https://docs.pingcap.com/tidb/stable/tiup-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb tiup cluster management

TiUP is the package manager for the TiDB ecosystem (from TiDB 4.0). You run a component with `tiup <component>[:version]`; if the component is missing locally, the latest stable version is downloaded from the mirror.

Install (macOS or Linux):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup --version
```

It installs into the `.tiup` folder under your home directory and adds its `bin` directory to `PATH` in your shell profile. Telemetry is disabled by default from TiUP v1.11.3.

Commands (implemented inside TiUP) versus components (independent packages):
- install, list, uninstall, update, status, clean, mirror, telemetry, env, history, link, unlink, help, completion.
- Components: `playground` (local TiDB cluster), `client`, `cluster` (production deployment), `bench` (stress tests); more appear in `tiup list`.

Examples from the help text:

```bash
tiup playground            # quick start
tiup playground nightly    # latest nightly
tiup install <component>[:version]
tiup update --all
tiup update --self
tiup list                  # available components
tiup status                # running/terminated instances
tiup clean --all
```

`tiup mirror` clones a private mirror from the official one. `tiup history` shows past executions (100 lines by default). Add `--help` to any command for details.

## Checked

2026-11-04. Confirmed against the TiUP Overview page: install command and location, telemetry default from v1.11.3, command and component lists, help examples, history default of 100 lines. Removed the claim that mirrors suit offline networks (not on the page).
Method: documentation only; no commands were run.
