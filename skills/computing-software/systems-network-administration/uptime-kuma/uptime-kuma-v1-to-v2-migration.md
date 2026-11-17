---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-v1-to-v2-migration
name: uptime-kuma-v1-to-v2-migration
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [uptime-kuma-v2, migration, breaking-changes, heartbeat-aggregation, liquidjs, backup-data-directory]
level: advanced
status: docs-checked
description: "Plan the Uptime Kuma v1 to v2 upgrade: backups, interrupted-migration risk, breaking changes in badges, retries and email templates."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma v1 to v2 migration

Before: stop the instance and back up the `data` directory (the guide says to do it three times). The migration aggregates the heartbeat table into a new format and can take minutes to hours (one example: 20 monitors with 90 days of data took about 7 minutes). Never interrupt it; if interrupted, restore the backup and retry.

Breaking changes:
- Badge `:duration` for ping and uptime accepts `24`, `24h`, `30d`, `1y` style values only, with limits of 720 hours, 1440 minutes or 365 days.
- Legacy browsers dropped.
- Backup/Restore from JSON removed: backing up the `data` directory is the only supported backup.
- DNS cache for HTTP monitors removed (the guide suggests bundled `nscd` for Docker).
- Default retries for newly created monitors changed from 1 to 0.
- Email (SMTP) notification templates now use LiquidJS: variables are case-sensitive and unmatched variables are ignored; supported are `name`, `msg`, `status`, `heartbeatJSON`, `monitorJSON`, `hostnameOrUrl`.

Docker-only: Alpine-based images are dropped (migration still works); do not upgrade on Debian/Raspbian Buster because of a libseccomp2 bug. Non-Docker: Node.js 14, 16 and 18 are dropped; 20.4 or newer is required.

Steps (Docker): `docker stop uptime-kuma`, back up data, run with `louislam/uptime-kuma:2`, then `docker logs -f uptime-kuma` to watch the migration. Compose: `docker compose down`, change the tag, `docker compose up -d`, `docker compose logs -f`. Non-docker: `pm2 stop uptime-kuma`, check `node --version`, then follow the update procedure. Avoid rootless images for this upgrade.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Migration From v1 To v2 page (breaking changes, limits, Docker, Compose and non-Docker steps, Node.js 20.4, rootless warning). Removed: The generic verify line.

Method: documentation only; no commands were run.
