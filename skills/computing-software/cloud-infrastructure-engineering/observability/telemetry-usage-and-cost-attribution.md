---
id: computing-software.cloud-infrastructure-engineering.observability.telemetry-usage-and-cost-attribution
name: telemetry-usage-and-cost-attribution
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [usage-insights, cost-attribution, billing-dashboards, observability-cost, chargeback]
level: advanced
status: draft
description: "Attribute observability spend to teams: per-team series, log bytes and span counts, Grafana Cloud usage insights and billing dashboards, cost labels, and showback reports."
sources: ["https://grafana.com/docs/grafana-cloud/cost-management-and-billing/", "https://grafana.com/docs/grafana-cloud/cost-management-and-billing/analyze-costs/", "https://grafana.com/docs/mimir/latest/configure/configure-cost-attribution/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Usage insights and cost attribution

## Pick the attribution key
One label present on every signal: `team` or `cost_center` (or derive from namespace via an ownership map).
Enforce it at ingest: Prometheus relabel from Kubernetes namespace labels, OTel `k8sattributes` +
`transform` setting `resource.attributes["team"]`, Alloy `discovery.relabel`.

## Measure per signal
- **Metrics (active series)**: `count by (team) ({__name__=~".+"})` is too expensive on large tenants; use
  Mimir **cost attribution** (`cost_attribution_labels: team` in tenant overrides) which exports
  `cortex_ingester_attributed_active_series{team=...}` and `cortex_distributor_received_attributed_samples_total`.
  On Prometheus: TSDB status API `/api/v1/status/tsdb` shows top label values by series.
- **Logs (bytes)**: Loki `sum by (team) (bytes_over_time({team=~".+"}[1d]))`; Loki per-tenant
  `loki_distributor_bytes_received_total`; Grafana Cloud "Usage insights" -> logs by label.
- **Traces (spans/bytes)**: spanmetrics `sum by (team) (rate(traces_spanmetrics_calls_total[1d]))` or collector
  `otelcol_exporter_sent_spans` per pipeline/tenant.

## Grafana Cloud
- Billing/usage dashboards (`grafanacloud-usage` data source): billable series, log GB, trace GB, overages.
- Cost management -> Attributions: configure the label and see per-value spend.
- Adaptive Metrics recommendations show which unused series to aggregate.

## Showback report
Weekly dashboard per team: active series, top 10 metrics by series, log GB/day with top streams, spans/day,
trend vs last month, and $ using contract unit prices. Put it in the team's own folder and post monthly.

## Guardrails that follow from attribution
Per-tenant limits (`max_global_series_per_user`, `ingestion_rate_mb`) or per-team budgets with alerts at 80%.

## Gotchas
- Untagged telemetry ends up in `__unattributed__`/empty - alert on its share growing.
- Cost attribution label cardinality is capped (`max_cost_attribution_cardinality`); use team, not service.
