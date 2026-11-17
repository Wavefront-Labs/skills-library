---
id: computing-software.cloud-infrastructure-engineering.cortex.federated-rule-groups
name: federated-rule-groups
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ruler, federation, source-tenants, multi-tenant, experimental]
level: advanced
status: docs-checked
description: "Evaluate ruler rule groups across several tenants with source_tenants while writing results to one tenant."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/ruler-tenant-federation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Federated rule groups are experimental. A federated group is a normal rule group with a `source_tenants` field listing tenants to query:

```yaml
name: cortex-admin
interval: 1m
source_tenants: [team-a, team-b, team-c]
rules:
  - record: tenant:prometheus_rule_evaluation_failures:rate5m
    expr: sum by (__tenant_id__) (rate(prometheus_rule_evaluation_failures_total[5m]))
```

The group is owned by the tenant that created it through the Ruler API (for example `infra`). Each rule is evaluated with `X-Scope-OrgID` set to `team-a|team-b|team-c`, exactly like a federated query, and series carry a `__tenant_id__` label (not added when only one source tenant is listed). Resulting series, `ALERTS` and `ALERTS_FOR_STATE` series and notifications are written to the owning tenant only; source tenants are never modified and cannot see the group. Groups without `source_tenants` are unaffected. An alerting rule fires once per source tenant that meets the condition, and alerts go to the owning tenant's Alertmanager configuration.

Enable with `-tenant-federation.enabled=true` (on all Cortex services) plus `-ruler.enable-federated-rules=true`, and restrict with `-ruler.allowed-federated-tenants` and `-ruler.disallowed-federated-tenants`. Federated groups need an object-store rule store; the `local` and `configdb` stores cannot carry `source_tenants`.

## Checked

Method: docs-checked 2026-11-09 against the Cortex ruler tenant federation guide (raw markdown, read in full).
