---
id: computing-software.cloud-infrastructure-engineering.datadog.audit-trail
name: audit-trail
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, audit-trail, audit-events, configuration-changes, compliance]
level: practitioner
status: docs-checked
description: "Use Audit Trail to see who changed monitors, dashboards, keys and settings, and alert on risky events."
sources: ["https://docs.datadoghq.com/account_management/audit_trail/", "https://docs.datadoghq.com/account_management/audit_trail/events/", "https://docs.datadoghq.com/account_management/api-app-keys/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit Trail
Goal: know who changed what.

```
# Organization Settings > Audit Trail Settings (under Compliance) > Enable
# Audit Explorer queries (Notable Events examples from the docs):
@evt.name:"Log Management" @asset.type:index
@evt.name:"Log Management" @asset.type:"exclusion_filter"
@evt.name:"Synthetics Monitoring" @asset.type:synthetics_test @action:(created OR deleted)
is_notable_event:true
```

- Enabling needs the `Audit Trail Write` permission; viewing events in Audit Explorer needs `Audit Trail Read`.
- Audit events behave like logs in the Log Explorer: filter by event name, actor, API key ID, user email, status and method, and inspect attributes such as `usr.email` and `client.ip`.
- The Inspect Changes (Diff) tab compares dashboard, notebook and monitor configuration before and after a change.
- Retention is optional to set: choose 3, 7, 15, 30 or 90 days. The default is 90 days when enabled and resets to 7 days if Audit Trail is disabled.
- Create monitors from audit event types or attributes (Audit Trail monitor), and analyse events with Cloud SIEM.
- Archiving (optional) writes to Amazon S3, Google Cloud Storage or Azure Storage for a SIEM to read; uploads happen every 15 minutes.
- CSV download is limited to 100K audit events.
- API key auditing: logs carry a `datadog.api_key_uuid` tag showing which key collected them.

Gotcha: audit events include user emails and client IPs, so restrict who holds `Audit Trail Read`. Application keys are not transferable between users; share one through a service account (keys page).

## Verify
- Delete a test dashboard and find the event, with your user and timestamp, in Audit Trail.

## Checked
2026-11-09. Confirmed against the Audit Trail overview page (enabling, Audit Trail Read and Write permissions, retention options and defaults, archiving targets and 15-minute cadence, Notable Events queries, Inspect Changes, API key auditing, monitors, Cloud SIEM, 100K CSV limit, usr.email and client.ip attributes) and the API keys page (service accounts for sharing). Removed: the invented `@evt.name:"Monitor"`, `"Authentication"` and `"API Keys"` example queries, the "forward via Log Archives" claim as worded, the claim that API-created changes show only the application key owner, and the quarterly-review advice about query names evolving.
Method: documentation only; no commands were run.
