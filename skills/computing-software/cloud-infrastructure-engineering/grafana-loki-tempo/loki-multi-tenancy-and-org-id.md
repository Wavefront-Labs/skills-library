---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-multi-tenancy-and-org-id
name: loki-multi-tenancy-and-org-id
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-multi-tenancy, loki, x-scope-orgid, auth_enabled, tenant-federation, per-tenant-isolation]
level: practitioner
status: docs-checked
description: "Run Loki multi-tenant with auth_enabled, the X-Scope-OrgID header, valid tenant IDs and multi-tenant queries."
sources: ["https://grafana.com/docs/loki/latest/operations/multi-tenancy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: isolate teams' logs and limits on one cluster.

```yaml
auth_enabled: true   # default; flag -auth.enabled
```
Every request then needs the header `X-Scope-OrgID: <tenant>`; without it Loki returns HTTP 401 with `no org id`. The docs show a reverse proxy adding the header (see their "Manage authentication" page).

With `auth_enabled: false` Loki uses one tenant whose ID is `fake`, and the header is not required.

Multi-tenant queries: set the querier option `multi_tenant_queries_enabled: true` (flag `-querier.multi-tenant-queries-enabled`, default false), then send several tenants in the header, separated by `|`:
```
curl -H 'X-Scope-OrgID: team-a|team-b' 'http://loki:3100/loki/api/v1/labels'
```
- Only query endpoints support this; push, tail and OTLP logs return 400 when more than one tenant is given.
- Results gain a `__tenant_id__` label (only when the query spans tenants); filter on it in the selector, for example `{app="foo", __tenant_id__=~"a.+"}`. Filtering on it in a pipeline stage is not supported. A stream's own `__tenant_id__` label is renamed with the prefix `original_`.

Tenant ID rules: at most 150 bytes; letters, digits, and the characters `! - _ . * ' ( )`; `.` and `..` alone are invalid. Do not put a colon in the header: components treat it inconsistently.

Per-tenant limits go in the runtime overrides (see the limits skill).

## Verify
```
curl -H "X-Scope-OrgID: team-a" "http://loki:3100/loki/api/v1/labels"
curl "http://loki:3100/loki/api/v1/labels"   # 401 no org id when auth_enabled is true
```

## Checked
2026-11-03. Confirmed against the Loki "Manage tenant isolation" page and the configuration reference (`multi_tenant_queries_enabled`, runtime overrides). Corrected: the old `tenant_federation.enabled` option does not appear in the docs; the option is `multi_tenant_queries_enabled`. Removed: the Alloy `loki.write` example, Grafana data source header steps, the claim that switching `auth_enabled` makes old data inaccessible, and the "avoid `/` and `|`" rule (replaced by the documented character set).
Method: documentation only; no commands were run.
