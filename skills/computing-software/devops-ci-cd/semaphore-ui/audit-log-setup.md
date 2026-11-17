---
id: computing-software.devops-ci-cd.semaphore-ui.audit-log-setup
name: audit-log-setup
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [audit-log, siem, trusted-proxy, retention, compliance, semaphore-ui]
level: advanced
status: docs-checked
description: "Enable the audit log, set instance_id, record real client IPs behind proxies and set retention_days."
sources:
  - https://semaphoreui.com/docs/admin-guide/audit-log
  - https://semaphoreui.com/docs/reference/audit-events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Audit log

Goal: record who did what for investigation or a SIEM.

The audit log covers sign-ins and failures, account and role changes, project object changes, task starts (with trigger), approvals and stops, runner registrations, exports and server starts. Passwords, tokens, secret values and task output never appear. Filtering, file export and SIEM forwarding need Pro; basic recording is in every edition.

Enable:

```json
{ "audit": { "enabled": true, "instance_id": "prod-eu" } }
```

Variables: `SEMAPHORE_AUDIT_ENABLED=true`, `SEMAPHORE_AUDIT_INSTANCE_ID=prod-eu`. The instance ID is 1-255 characters without spaces and is added to every event. Restart; earlier actions are not recorded.

Behind a reverse proxy, events would show the proxy address. List proxy networks to read `X-Forwarded-For` or `X-Real-IP` only from them:

```json
{ "audit": { "trusted_proxy_cidrs": ["10.0.0.0/8"] } }
```

Never list networks where users connect from, or they could spoof addresses.

Retention (default keeps everything), deleted hourly:

```json
{ "audit": { "retention_days": 365 } }
```

Events live in the database, so normal backups include them. A partially failed request is recorded as success with `metadata.partial=true`.

Verify: change a template and find the event with your address in the audit view.

## Checked

2026-11-04: checked against the audit log page and the audit events reference. Every claim is stated there.

Method: documentation only; no commands were run.
