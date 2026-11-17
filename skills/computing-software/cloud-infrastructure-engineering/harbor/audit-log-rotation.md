---
id: computing-software.cloud-infrastructure-engineering.harbor.audit-log-rotation
name: audit-log-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [log-rotation, audit-log-purge, syslog-endpoint, purge-history, harbor]
level: practitioner
status: docs-checked
description: "Schedule audit log purge in Harbor, choose event types and retention window, dry-run, forward purged records to syslog, and stop runs."
sources:
  - https://goharbor.io/docs/main/administration/log-rotation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log rotation purges old audit logs and can forward them to a syslog endpoint.

Under Administration, **Clean Up**, **Log Rotation** tab:
1. Choose a schedule: None, Hourly, Daily (midnight), Weekly (midnight every Saturday) or Custom (`cron`).
2. **Keep records in**: Hours or Days. With 7 days, only logs 8 or more days old are purged.
3. **Event types to purge**: Create artifact, Delete artifact and Pull artifact; only selected types are included.
4. **Save**.

**DRY RUN** writes a log with the estimated amount to purge, viewable in the Purge History table. **PURGE NOW** runs a purge immediately. Purge History shows Task ID, Trigger Type, Dry Run, Status, Creation Time, Update time and Logs.

Forwarding: under Configuration, System Settings, set **Audit Log Forward Syslog Endpoint**. For a docker-compose install the local endpoint is `harbor-log:10514`. Harbor forwards all purged records to that endpoint. If forwarding is configured you may also tick **Skip Audit Log Database** so records go only to syslog.

To stop a purge, tick its Task ID in Purge History, click **Stop** and confirm. This stops further processing only; logs already purged are not restored.

## Checked

2026-11-03. Schedule options, the 7-day example, event types, DRY RUN and PURGE NOW, Purge History columns, the syslog endpoint `harbor-log:10514`, Skip Audit Log Database and the stop procedure were read against the Harbor docs page Log Rotation. Nothing removed.

Method: documentation only; no commands were run.
