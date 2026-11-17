---
id: computing-software.cloud-infrastructure-engineering.observability.per-team-cardinality-budgets-and-chargeback
name: per-team-cardinality-budgets-and-chargeback
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [cardinality-budget, telemetry-chargeback, observability-cost, cardinality, usage-insights, mimir]
level: advanced
status: draft
description: "Set per-team active-series and log-volume budgets, enforce them with tenant limits and report usage back to teams for chargeback or showback."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-custom-trackers/", "https://grafana.com/docs/mimir/latest/configure/about-runtime-configuration/", "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Per-team cardinality budgets and chargeback

## Attribute usage
- Require a `team` label (or tenant per team) on every target via relabeling or OTel resource attribute.
- Prometheus: `count by (team) ({__name__=~".+"})` is expensive; run it rarely, or use `/api/v1/status/tsdb` for top metrics and map metric prefixes to teams.
- Mimir: custom active series trackers per tenant in runtime config:
```yaml
overrides:
  tenant-a:
    active_series_custom_trackers:
      team_payments: '{team="payments"}'
      team_search: '{team="search"}'
```
Exposes `cortex_ingester_active_series_custom_tracker{name="team_payments"}`.
- Loki: `sum by (team) (rate(loki_distributor_bytes_received_total[1h]))` per tenant, or volume API by label.

## Budget and enforcement
1. Baseline 30 days of usage per team; set budget = baseline + growth allowance.
2. Soft limit: alert at 80% to the team's channel.
3. Hard limit: per-tenant `max_global_series_per_user` (Mimir) or per-job `sample_limit` (Prometheus scrape) so one team cannot take down shared ingestion.
4. Monthly report: series, samples/s, log GB, cost per unit, top 10 metrics per team.

## Showback vs chargeback
Start with showback (visible cost, no billing). Move to chargeback only when teams have tools to reduce (dropping rules, adaptive metrics recommendations).

## Gotchas
- Hard limits drop data at the worst time (incidents raise cardinality). Leave headroom and alert before the cap.
- A missing team label must route to a default owner, not be ignored.

## Verify
- [ ] Every active series is attributable to a team (unattributed < 5%).
- [ ] Teams receive monthly usage reports and an alert before hitting limits.
