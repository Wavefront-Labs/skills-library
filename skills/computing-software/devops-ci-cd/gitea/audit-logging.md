---
id: computing-software.devops-ci-cd.gitea.audit-logging
name: audit-logging
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-audit-log, gitea, audit-record-output, audit-retention-days, audit-jsonl-export, delete-old-audit-events]
level: advanced
status: docs-checked
description: "Enable Gitea audit logging to the database, view and export events as JSONL, understand event fields, actors, what is not recorded and retention pruning."
sources: ["https://docs.gitea.com/administration/audit-logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea audit logging

Structured records of security-relevant events (action, actor, scope, origin, message, JSON metadata). **Off by default**, and when off request behaviour is unchanged. It is separate from the app/router/access logs in `gitea-log-writers`.

```ini
[audit]
RECORD_OUTPUT = database
RETENTION_DAYS = 30
```
Restart after changing. Invalid `RECORD_OUTPUT` falls back to `disabled`. Docker: `GITEA__audit__RECORD_OUTPUT=database`, `GITEA__audit__RETENTION_DAYS=30`.

## Where to view
Pages exist even when recording is off (they list earlier events; admin page shows a warning): admins at `/-/admin/monitor/audit_logs` (every event), users at `/user/settings/audit_logs`, org owners at `/<org>/settings/audit_logs`, repo admins at `/<owner>/<repo>/settings/audit_logs`. Filter by actor, action (exact or family prefix such as `user:impersonation`, `repository:webhook`) and origin. Admins can **Export JSONL** (`gitea-audit-log-<timestamp>.jsonl`).

## Event fields
`action` (stable colon-separated id like `repository:archive`, `user:accesstoken:add`), `actor` (impersonation records both users), actor credential kind and id never the secret (`access-token:<id>`, `oauth2-grant:<id>`, `gitea-actions:<task id>`, `deploy-key:<key id>`), `scope` (user, organization, repository, system), `origin` (ui, api, cli, system), message, metadata (no secrets), IP address (SSH client address for SSH pushes, `127.0.0.1` for HTTP pushes), timestamp. `system:startup` message stays `System started [Gitea {version}]` so it can be parsed.
System actors: `(gitea-cli)` (admin commands and startup/shutdown, origin cli), `(gitea-auth-source)`, `gitea-actions`, `(deploy-key)`, `(Cron)`, `Unknown`.

## Coverage and gaps
Recorded: user, org and repository changes, issue/PR create, delete, comments and merges, projects and wiki, Actions enable/disable/dispatch, system settings. **Not** recorded: reads (browse, clone, fetch, API GET), logins other than failed 2FA (use the access log and fail2ban), issue/PR edits, secret values, which SSH key a normal user pushed with. A failed audit write is logged and never fails the request.

## Retention
`RETENTION_DAYS` default 30, `0` keeps forever. Pruning is the `cron.delete_old_audit_events` task (`SCHEDULE` `@every 24h`, `OLDER_THAN` defaults to the retention), registered only while recording is on and `RETENTION_DAYS > 0`. Turning recording off also stops pruning, so old rows remain.

## Checked

2026-11-03: read https://docs.gitea.com/administration/audit-logging/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Corrected the system actor names to the documented `(gitea-cli)`, `(gitea-auth-source)`, `(deploy-key)`.
Method: documentation only; no commands were run.
