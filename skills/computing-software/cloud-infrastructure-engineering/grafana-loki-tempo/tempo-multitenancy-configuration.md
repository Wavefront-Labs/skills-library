---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tempo-multitenancy-configuration
name: tempo-multitenancy-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tempo-multitenancy, tempo, multitenancy-enabled, x-scope-orgid, per-tenant-overrides, tenant-isolation]
level: practitioner
status: docs-checked
description: "Enable Tempo multi-tenancy with the X-Scope-OrgID header, tenant-aware Alloy export, Grafana data source header and per-tenant overrides."
sources: ["https://grafana.com/docs/tempo/latest/operations/manage-advanced-systems/multitenancy/", "https://grafana.com/docs/tempo/latest/configuration/tenant-ids/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: isolate trace data and limits per team.

`X-Scope-OrgID` carries the tenant ID and scopes writes (each span stored under its tenant) and reads (only that tenant's data). Enable on every Tempo component:
```yaml
multitenancy_enabled: true      # or: tempo --multitenancy.enabled=true
```
Then every request must include the header.

Tenant ID rules: at most 150 bytes; only `0-9 a-z A-Z ! - _ . * ' ( )`; case-sensitive; not empty; `.` and `..` are invalid. Cross-tenant queries are supported for search, search-tags and trace-by-ID.

Alloy exporter sending a tenant:
```
otelcol.exporter.otlphttp "tempo" {
  client {
    endpoint = "http://tempo:4318"
    headers = { "X-Scope-OrgID" = "<TENANT>" }
    tls { insecure = true }
  }
}
```
OpenTelemetry Collector: `exporters.otlp.headers.x-scope-orgid`. Grafana Tempo data source provisioning: `jsonData.httpHeaderName1: "X-Scope-OrgID"` with `secureJsonData.httpHeaderValue1: "<TENANT>"`.

Per-tenant limits and retention come from a runtime overrides file, reloaded without restart:
```yaml
# tempo.yaml
overrides:
  per_tenant_override_config: /conf/overrides.yaml
```
```yaml
# overrides.yaml
overrides:
  "tenant-a":
    compaction:
      block_retention: 24h
    ingestion:
      rate_limit_bytes: 4000000
      burst_size_bytes: 20000000
      max_traces_per_user: 10000
    global:
      max_bytes_per_trace: 30000000
```
Global defaults in the configuration reference: `rate_limit_bytes` and `burst_size_bytes` 30 MB, `max_bytes_per_trace` 5 MB.

Gotchas
- Set every field you want to keep in a tenant's overrides: unset fields become zero values, not your main-config defaults (a `0s` retention effectively disables block retention for that tenant).
- Tempo 3.0 disables legacy flat overrides unless `enable_legacy_overrides: true`; use the scoped format above.
- The metrics-generator forwards `X-Scope-OrgID` to remote write by default.

## Verify
A request with the header returns that tenant's data; with multi-tenancy on, requests without the header are not valid.

## Checked
2026-11-03. Confirmed against the Tempo "Enable multi-tenancy" page, the tenant IDs page, the configuration reference (ingestion and global defaults) and the metrics-generator multitenancy page. Removed: the `ingestion`/`global` limits claimed for `team-a` that were not on the page, "Tempo does not authenticate" and "switching on later hides data" remarks, the `single-tenant` name claim and the curl check.
Method: documentation only; no commands were run.
