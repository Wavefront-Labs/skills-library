---
id: computing-software.devops-ci-cd.rundeck.audit-trail-log
name: audit-trail-log
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, audit-trail, audit-events-log, siem, login-failed]
level: practitioner
status: docs-checked
description: "Read the Rundeck audit trail file rundeck.audit.events.log: event structure, action types, and options for shipping events to external systems."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/audit-trail.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 4.6.0 Rundeck writes `rundeck.audit.events.log` in the default log directory (see `framework.properties`).

Each line is one `AuditEvent` with four parts:
- `ResourceInfo`: `resourceType` and `resourceName`, for example a user, project, job or `system_acl`. For a job `run` the name carries project, job UUID, group/name and the execution id (for example `TestProject:<uuid>:jobgroup/testjob:15032`).
- `ActionType`: seen in the docs example as `login_success`, `login_failed`, `logout`, `view`, `create`, `update`, `delete`, `run`.
- `UserInfo`: `username` and `userRoles`.
- `RequestInfo`: `serverHostname`, `serverUUID`, `sessionID`, `userAgent`.

Quick checks:
- failed logins: search for `ActionType='login_failed'`
- who ran what: `ActionType='run'` with the `username`
- ACL edits: `resourceType='system_acl'`

Shipping the events:
1. All editions: forward the file with Filebeat/Logstash, Fluentd/Fluent Bit, Splunk Universal Forwarder or a script. The format is not structured JSON, so expect regex parsing, and you must configure rotation and file monitoring yourself.
2. Enterprise 5.13.0+: Audit Stream Plugin streams structured JSON in real time (Datadog, New Relic, Splunk, webhooks).
3. Developers: write a custom audit event listener plugin.

Verify by logging in and out and confirming new `login_success` and `logout` lines appear.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Audit Trail Log: file rundeck.audit.events.log since 4.6.0, the four event components, the ActionType values shown in the example, the run resourceName format with execution id, and the three integration options including Enterprise 5.13.0+ Audit Stream Plugin. Nothing removed.

Method: documentation only; no commands were run.
