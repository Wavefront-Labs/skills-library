---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mimir-multi-tenant-alertmanager
name: mimir-multi-tenant-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mimir-alertmanager-config, multi-tenant-alertmanager, mimir, alertmanager, mimirtool]
level: advanced
status: docs-checked
description: "Run Mimir's multi-tenant Alertmanager: per-tenant config upload via mimirtool and API, fallback config, sharding, limits, ruler wiring and Grafana integration."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/components/alertmanager/", "https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/", "https://grafana.com/docs/mimir/latest/references/http-api/#alertmanager"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mimir multi-tenant Alertmanager

Mimir embeds Alertmanager with per-tenant configuration, stored in object storage and sharded across replicas.

## Config
```yaml
alertmanager:
  data_dir: /data/alertmanager
  external_url: https://mimir.example.com/alertmanager
  fallback_config_file: /configs/fallback.yaml   # overrides the built-in fallback for tenants with no config
  sharding_ring:
    replication_factor: 3
alertmanager_storage:
  backend: s3
  s3: {bucket_name: mimir-alertmanager}
ruler:
  alertmanager_url: http://mimir-alertmanager/alertmanager    # or dnssrvnoa+ for all replicas
```
Alert state is stored on local disk (`-alertmanager.storage.path`) and periodically in the storage backend; a restarting replica first tries to load state from its peers. Without replication, persist that directory to avoid losing alert state.

## Per-tenant config
```bash
mimirtool alertmanager load alertmanager.yaml templates/*.tmpl --address=$MIMIR --id=team-a
mimirtool alertmanager get --address=$MIMIR --id=team-a
mimirtool alertmanager verify alertmanager.yaml
```
API: `POST /api/v1/alerts` with body `{alertmanager_config: "<yaml>", template_files: {name: content}}` and header
`X-Scope-OrgID: team-a`. UI per tenant at `/alertmanager` (with the tenant header via a proxy).

## Limits (overrides)
`alertmanager_max_config_size_bytes`, `alertmanager_max_templates_count`, `alertmanager_max_alerts_count`,
`alertmanager_max_dispatcher_aggregation_groups`, `alertmanager_notification_rate_limit` and per-integration
`alertmanager_notification_rate_limit_per_integration` (all per-tenant limits with the `alertmanager` prefix). Receivers can be restricted
(`alertmanager_receivers_firewall_block_cidr_networks`) to stop tenants calling internal IPs.

## Grafana
Add a Grafana Alertmanager data source pointing at Mimir with the `X-Scope-OrgID` tenant header; check the Grafana data source docs for the current option names.

## Gotchas
- Config uses the same file format as the Prometheus Alertmanager.
- UTF-8 matcher support is opt-in (Mimir 2.12 and later, `utf8-strict-mode-enabled`); enabling then disabling strict mode can break tenant configs that used UTF-8.
- A default fallback configuration always exists for tenants without their own config; override it with `fallback_config_file`.
- Set `--address` to the host only (default `-server.path-prefix` is `/`), not `/alertmanager`.

## Verify
Send a test alert for the tenant (with the tenant ID header) and confirm the receiver gets it; the tenant's UI at `/alertmanager` shows the alert.

## Checked
- 2026-10-28. Confirmed against the Mimir Alertmanager architecture page (multi-tenancy via tenant ID header, fallback configuration and `-alertmanager.configs.fallback`, hash ring sharding, alert state storage, `-ruler.alertmanager-url`, `mimirtool alertmanager get`, `--address` host-only note, UTF-8 opt-in from 2.12), the HTTP API page (`POST /api/v1/alerts`, `alertmanager_config`, `template_files`) and the configuration reference (`sharding_ring.replication_factor` default 3, the `alertmanager_*` per-tenant limits).
- Removed: the RF=1 silences claim, the `http_config` remark, the Grafana data source option names, the `amtool` step and `cortex_alertmanager_notifications_total`; corrected the no-fallback gotcha (a default fallback always exists).
Method: documentation only; no commands were run.

