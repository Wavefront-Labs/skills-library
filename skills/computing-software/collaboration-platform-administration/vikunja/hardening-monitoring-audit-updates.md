---
id: computing-software.collaboration-platform-administration.vikunja.hardening-monitoring-audit-updates
name: hardening-monitoring-audit-updates
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, audit-log, structured-logging, security-advisories, version-pinning, restore-test]
level: advanced
status: docs-checked
description: "Operate Vikunja securely over time: protect health and metrics endpoints, ship structured logs, enable the Pro audit log, test restores and pin versions."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/security-hardening.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoints: `/health` is unauthenticated and returns only `OK` or an error depending on database and Redis reachability. The metrics endpoint `/api/v1/metrics` is public unless both `metrics.username` and `metrics.password` are set; set both or block the path at the proxy. Never enable `metrics.pprof` on an internet-reachable instance.

Logging: `log.format: structured` for JSON to a central collector. For files use `log.standard: file`, `log.http: file` and `log.path`.

Audit log (Pro feature): `audit.enabled: true` writes JSON lines to `audit.logfile` (default `audit.log` in the log path) for logins, API token use and changes to tasks and projects. Without a valid license nothing is written. The file is created with mode `0600` and its directory `0750`; entries are unsigned, so ship them off-host. `audit.rotation.maxsizemb` (100) and `maxage` (30 days) rotate and prune but are not retention policy. Entries use IDs only, no names or content.

Backups: back up database and files together, encrypt, store off-host, and test restores by logging in and opening a task with an attachment.

Updates: watch GitHub releases or the changelog RSS, read security advisories, pin versions (not `latest`), and back up before every upgrade because migrations run on start. Report vulnerabilities to security@vikunja.io.

## Checked

2026-11-04. Confirmed against the Vikunja Security hardening page (setup/security-hardening): health and metrics endpoints, metrics.pprof warning, logging keys, the Pro audit log behaviour, file modes and rotation defaults, backups, update advice and the report address. Nothing removed.

Method: documentation only; no commands were run.
