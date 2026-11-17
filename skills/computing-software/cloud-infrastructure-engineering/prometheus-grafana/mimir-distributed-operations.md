---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mimir-distributed-operations
name: mimir-distributed-operations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-mimir, mimir-distributed-helm, mimir-helm-values, mimir-limits-overrides, runtime-config-mimir, mimir-ha-tracker, ha-dedup-config, shuffle-sharding, mimir-sharding, mimirtool-rules, mimirtool-analyze, mimirtool-backfill, mimir-otlp, otlp-to-mimir]
level: advanced
status: docs-checked
description: "Operate mimir-distributed: Helm values, per-tenant limits via runtime config, HA tracker dedup for Prometheus pairs, shuffle sharding, OTLP ingestion, and mimirtool."
sources: ["https://grafana.com/docs/mimir/latest/set-up/helm-chart/", "https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/", "https://grafana.com/docs/mimir/latest/configure/configure-shuffle-sharding/", "https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/", "https://grafana.com/docs/mimir/latest/configure/configure-otel-collector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operating mimir-distributed

## Helm (grafana/mimir-distributed)
Start from the chart's sizing presets (`small.yaml`, `large.yaml`), then:
```yaml
mimir:
  structuredConfig:
    common:
      storage: {backend: s3, s3: {endpoint: s3.eu-west-1.amazonaws.com, region: eu-west-1}}
    blocks_storage: {s3: {bucket_name: mimir-blocks}}
    ruler_storage: {s3: {bucket_name: mimir-ruler}}
    alertmanager_storage: {s3: {bucket_name: mimir-alertmanager}}
    limits:
      accept_ha_samples: true
      ha_cluster_label: cluster
      ha_replica_label: __replica__
    distributor:
      ha_tracker: {enable_ha_tracker: true, kvstore: {store: memberlist}}
runtimeConfig:
  overrides:
    team-a: {ingestion_rate: 200000, max_global_series_per_user: 3000000, ingestion_tenant_shard_size: 6}
```

## HA dedup
Prometheus pairs send identical series with `cluster: prod-eu` and `__replica__: a|b` external labels. The
distributor accepts samples only from the elected replica per cluster and drops the label; it fails over after
`ha_tracker_failover_timeout` (30s default). To see which replica is elected, enable `-distributor.ha-tracker.enable-elected-replica-metric`.

## Shuffle sharding
Each tenant uses a subset of ingesters/store-gateways/queriers (`ingestion_tenant_shard_size`,
`store_gateway_tenant_shard_size`, `max_queriers_per_tenant`), limiting blast radius of a noisy tenant.
See the shuffle sharding guide for how to choose the shard size.

## OTLP
Endpoint `/otlp/v1/metrics` (OTLP/HTTP). Collector `otlphttp` exporter with `endpoint: https://mimir/otlp` and
tenant header. Resource attributes go to `target_info`; promote some to labels with
`promote_otel_resource_attributes` (per-tenant limit) and use `info()`/joins for the rest.

## mimirtool
```bash
mimirtool rules load --address=$MIMIR --id=team-a rules/*.yaml      # also: rules diff / sync / lint / prepare
mimirtool rules diff --address=$MIMIR --id=team-a rules/*.yaml
mimirtool analyze grafana --address=$GRAFANA --key=$TOKEN            # metrics used by dashboards
mimirtool analyze prometheus --address=$MIMIR --id=team-a            # used vs unused series
mimirtool backfill --address=$MIMIR --id=team-a ./blocks/            # upload TSDB blocks
mimirtool alertmanager load am.yaml --address=$MIMIR --id=team-a
```

## Verify
- [ ] `cortex_discarded_samples_total` by reason near zero; the `err-mimir-*` runbook entries explain each reason.
- [ ] Killing replica `a` of an HA pair keeps graphs continuous (replica `b` elected).
- [ ] Mimir mixin dashboards and alerts are healthy.

## Checked
- 2026-10-28. Confirmed against the Mimir configuration reference (`accept_ha_samples`, `ha_cluster_label`, `ha_replica_label` default `__replica__`, `ha_tracker`, `ha_tracker_failover_timeout` 30s, `ingestion_tenant_shard_size`), the HA deduplication, shuffle sharding and OpenTelemetry collector pages (`/otlp/v1/metrics`, `promote_otel_resource_attributes`), the Helm chart configuration page (`mimir.structuredConfig`) and the mimirtool page (`rules load|diff|sync|lint|prepare`, `analyze`, `backfill`, `alertmanager load`).
- Removed: `cortex_ha_tracker_elected_replica_changes_total`, the `per_user_series_limit` reason name, the shard-size rule of thumb and mixin dashboard names.
Method: documentation only; no commands were run.
