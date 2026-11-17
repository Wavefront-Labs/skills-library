---
id: computing-software.cybersecurity-defensive.zitadel.service-ping-telemetry
name: service-ping-telemetry
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, service-ping, telemetry, privacy, configuration]
level: practitioner
status: docs-checked
description: "Understand what ZITADEL's Service Ping sends and disable it entirely or per report in the runtime configuration."
sources:
  - https://zitadel.com/docs/self-hosting/manage/service_ping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service Ping periodically sends anonymized analytics and usage data to a central endpoint to help improve ZITADEL. It is enabled by default.

Base information is always sent while the feature is on: your system ID, the running ZITADEL version, and for every instance its id, creation date and domains. To stop that, disable the whole feature:

```yaml
ServicePing:
  Enabled: false # ZITADEL_SERVICEPING_ENABLED
```

The resource counts report adds counts of instances, organizations, projects and users per organization, machine users, SCIM provisioned users, instance administrators, identity providers, LDAP providers, actions, targets and executions, login policies, MFA enforcement, and password complexity, expiry, lockout and notification policies. The list may grow. Disable only this report with `ServicePing.Telemetry.ResourceCounts.Enabled: false`.

The interval is a cron expression, default `@daily`, randomized at startup so systems do not report at the same moment. It must be at least 30 minutes. For example `15 4 * * *` sends at 4:15 each day. `MaxAttempts` sets how many tries a failed report gets before giving up for that interval; other reports still run.

## Checked

2026-11-08. Read the service ping page in full; removed an unsupported advice line.

Method: documentation only; no commands were run.
