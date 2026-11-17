---
id: computing-software.collaboration-platform-administration.zulip.upgrade-troubleshooting-and-rollback
name: upgrade-troubleshooting-and-rollback
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [upgrade-rollback, upgrade-log, deployments-last, restart-server]
level: practitioner
status: docs-checked
description: "Troubleshoot a failed Zulip upgrade and roll back using the deployments last symlink, restart-server paths, upgrade.log, errors.log and the out-of-memory webpack fix."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrade troubleshooting and rollback

Upgrade scripts are idempotent, so retrying after fixing a cause is harmless. Common causes:

- Networking problems, such as unreliable Internet access or a missing proxy. Fix and retry.
- Out-of-memory failures on small hosts, especially with `upgrade-zulip-from-git`, where `tools/webpack` usually fails. Stop the server first with `./scripts/stop-server` to free RAM.

Logs:

- `/var/log/zulip/upgrade.log` holds all upgrade script output.
- `/var/log/zulip/errors.log` records Internal Server Errors.

Rollback applies to minor releases (for example 9.4 back to 9.3). Rolling a database migration back across major releases needs a more complicated process.

An upgrade creates a new directory under `~zulip/deployments/` containing a full copy of the Zulip code, then moves the symlinks `current`, `last` and `next`. So a bad release can be reversed quickly:

- Previous version: `~zulip/deployments/last/scripts/restart-server`
- An earlier one: `~zulip/deployments/DATE/scripts/restart-server`, using that deployment's directory name

`restart-server` stops any running Zulip server, then starts the version whose path you invoked.

By default only deployments from the last two weeks are kept when old ones are purged (`--skip-purge-old-deployments` skips purging). The general troubleshooting guide covers the wider set of service problems.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: the unsupported 'prepare ahead' advice; the two-week deployment retention figure is confirmed on production/system-configuration.html.

Method: documentation only; no commands were run.
