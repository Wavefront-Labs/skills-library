---
id: computing-software.cloud-infrastructure-engineering.harbor.audit-log-skip-and-forwarding
name: audit-log-skip-and-forwarding
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [audit-log, skip-audit-log-database, gdpr-audit-logs, audit-forwarding, harbor]
level: practitioner
status: docs-checked
description: "Control what Harbor keeps in its audit log database, which event types are recorded, and how deleted usernames are masked."
sources:
  - https://goharbor.io/docs/main/administration/audit-log/
  - https://goharbor.io/docs/main/administration/managing-users/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor records operations in an audit log that administrators view in the portal. After v2.13.0 the `Audit Logs` tab shows current records and the `Audit Logs(Legacy)` tab shows records from before v2.13.0. You can filter by operation type, username, operation, resource and resource type.

Recorded event types: pull artifact, push artifact, delete artifact, create/update/delete/login/logout user, change configuration, create/delete project, create/delete robot, and delete repository. Table columns are Timestamp, Username, Resource, Resource Type, Operation and Operation Description.

Three controls reduce database storage or protect identities:
- **Skip Audit Log Database**: if you configured an endpoint to forward audit logs, tick this box. Harbor then keeps no audit records in its database and forwards every log to the endpoint immediately.
- **Disable Audit Log Event Type**: go to Administration, Configuration, System Settings and check the event types to skip. Those events are no longer saved in the database. This does not require audit log forwarding to be configured.
- `GDPR_AUDIT_LOGS`: by default the audit log keeps a user name after the user is deleted. Enabling this setting replaces it with a checksum when the user is deleted. It is an environment variable of the core container (Helm value `core.gdpr.auditLogsCompliant`), not a UI setting, and applies only to users deleted after it is enabled.

Note: with Skip Audit Log Database selected Harbor keeps no audit records in its database, so the forwarding endpoint holds the only copy.

## Checked

2026-11-03. The v2.13.0 tab split, event types, table columns and the three controls were read against the Harbor docs page Audit Log; the GDPR variable details against Managing Users (Deleting Users in Compliance with GDPR). Removed: the "no working endpoint" wording, replaced by what the page states.

Method: documentation only; no commands were run.
