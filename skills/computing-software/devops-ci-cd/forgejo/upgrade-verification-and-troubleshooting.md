---
id: computing-software.devops-ci-cd.forgejo.upgrade-verification-and-troubleshooting
name: upgrade-verification-and-troubleshooting
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [upgrade-verification, doctor-check, debug-logging, db-version-guard]
level: practitioner
status: docs-checked
description: "Verify an upgraded instance with forgejo doctor, raise log levels and bisect failing multi-version jumps."
sources:
  - https://forgejo.org/docs/latest/admin/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Verification after an upgrade is critical: restoring the pre-upgrade backup is easy right away, but if a problem surfaces days or weeks later restoring is no longer an option and fixing a live instance is harder.

1. Run `forgejo doctor check --all --log-file /tmp/doctor.log` and make sure it reports no problem.
2. Walk through the web interface using a checklist of typical use cases so nothing is missed.
3. On any problem, raise the log level and read the logs. If the cause stays unclear, ask in the Forgejo chatroom before trying a fix.

For debug logs, put this in app.ini (removing other [log] sections): `[log]` with `LEVEL=debug`, `MODE=console,file`, `ROUTER=console,file`, `XORM=console,file`, `ENABLE_XORM_LOG=true`, `FILE_NAME=forgejo.log`, plus `[log.file.router]` and `[log.file.xorm]` sections with their own FILE_NAME. Setting `LOG_SQL=true` in the [database] section shows all SQL.

If a jump from x.y to x.y+2 fails, upgrade to the last release of each intermediate series (for example 1.19.4-0, then 1.20.6-0) and verify each, which shows which series causes the failure.

The database version is stored in the database to prevent accidental downgrades: an older Forgejo refuses to start on a newer schema.

## Checked

Date: 2026-11-07
Confirmed against the "Upgrade guide" page (forgejo.org/docs/latest/admin/upgrade/), read in full including its code blocks: the Verify Forgejo works steps (`forgejo doctor check --all --log-file /tmp/doctor.log`, manual web check, raise log level, ask in the chatroom), the debug `[log]` settings and `[log.file.router]`/`[log.file.xorm]` sections, `LOG_SQL=true` in `[database]`, the x.y to x.y+2 bisect example (1.19.4-0, 1.20.6-0), and the database version guard against downgrades.
Corrected: nothing needed; every claim matched the page text.
Method: documentation only; no commands were run.
