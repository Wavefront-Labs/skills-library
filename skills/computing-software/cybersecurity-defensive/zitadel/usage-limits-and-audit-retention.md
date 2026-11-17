---
id: computing-software.cybersecurity-defensive.zitadel.usage-limits-and-audit-retention
name: usage-limits-and-audit-retention
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, limits, quotas, system-api, audit-retention, virtual-instances]
level: advanced
status: docs-checked
description: "Block ZITADEL virtual instances and cap how far back audit events can be queried, using system API limits and DefaultInstance.Limits."
sources:
  - https://zitadel.com/docs/self-hosting/manage/usage_control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Self-hosted operators can limit usage per instance, for example to build a pricing model on virtual instances. These controls work at instance level.

Block an instance with the system API. Most requests to a blocked instance fail with HTTP 429 Too Many Requests, or gRPC status 8 Resource Exhausted. System API requests still work. Paths under `/ui/login` get a 302 redirect to `/ui/console`, where the user is guided to `InstanceManagementURL`. Blocked HTTP responses also set a cookie, so you can block traffic earlier, for example with a WAF rule. To block new instances by default, set `DefaultInstance.Limits.Block`.

```yaml
DefaultInstance:
  Limits:
    Block: # ZITADEL_DEFAULTINSTANCE_LIMITS_BLOCK
```

Audit retention: you can restrict the maximum age of events returned by the Events search and the history APIs for the current user, users, applications, organizations, projects and project grants. Set a global default with `AuditLogRetention` (environment variable `ZITADEL_AUDITLOGRETENTION`); `0s` means all events are available. An instance limit overrides the system default, and you can set a default for new virtual instances under `DefaultInstance.Limits`.

Limits can also be set for one specific virtual instance through the system API. The same page covers quotas on authenticated requests and action run seconds, which are off by default (`Quotas.Access.Enabled` and `Quotas.Execution.Enabled` are false).

## Checked

2026-11-08. Read the usage control page in full; removed an unsupported system-user advice line and added the quota defaults.

Method: documentation only; no commands were run.
