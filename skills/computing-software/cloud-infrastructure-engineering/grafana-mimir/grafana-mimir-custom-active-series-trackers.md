---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-custom-active-series-trackers
name: grafana-mimir-custom-active-series-trackers
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [active-series, custom-trackers, ingester, cardinality, metrics]
level: practitioner
status: docs-checked
description: "Shows how to count active series matching label patterns with Mimir custom trackers and read the cortex_ingester_active_series_custom_tracker metric."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-custom-trackers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom active series trackers

An ingester can count active series matching label matchers, per tenant. Define trackers with `-ingester.active-series-custom-trackers` or YAML:

```yaml
active_series_custom_trackers:
  dev: '{namespace=~"dev-.*"}'
  prod: '{namespace=~"prod-.*"}'
```

## Output

Each ingester exposes `cortex_ingester_active_series_custom_tracker` on `/metrics` with labels `name` (the tracker name) and `user` (tenant):

```text
cortex_ingester_active_series_custom_tracker{name="prod", user="tenant_1"} 10
```

Each tracker produces up to one series per tenant, so many trackers times many tenants multiplies metric cardinality.

## Per-tenant override

```yaml
overrides:
  tenant_with_only_prod_metrics:
    active_series_custom_trackers:
      service1: '{service="service1"}'
      service2: '{service="service2"}'
```

An override replaces that tenant's default trackers.

## Reading totals

Each ingester reports its own count. Sum across ingesters for a global figure, and with replication factor above 1 divide by the replication factor, since each series is held by that many ingesters.

## Checked

Confirmed against the page: flag and YAML form, metric name with `name` and `user` labels, per-tenant series, override example via runtime configuration, summing across ingesters and the replication factor adjustment. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-custom-trackers page (grafana/mimir main), read in full.
