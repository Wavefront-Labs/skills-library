---
id: computing-software.cloud-infrastructure-engineering.observability.modelling-observability-saas-pricing
name: modelling-observability-saas-pricing
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability-pricing-model, active-series-billing, observability-cost, telemetry-budget, vendor-evaluation]
level: practitioner
status: draft
description: "Translate telemetry volumes into vendor billing units (active series, DPM, GB ingested, hosts, spans) to forecast and compare observability SaaS costs."
sources: ["https://grafana.com/docs/grafana-cloud/cost-management-and-billing/understand-your-invoice/", "https://docs.datadoghq.com/account_management/billing/", "https://grafana.com/docs/grafana-cloud/cost-management-and-billing/understand-your-invoice/metrics-invoice/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modelling observability SaaS pricing

## Billing units you will meet
| Unit | Typical meaning | Measure it yourself with |
|---|---|---|
| Active series | distinct series seen in a period (often 95th percentile of hourly counts) | `prometheus_tsdb_head_series`, Mimir `cortex_ingester_active_series` |
| DPM (data points per minute) | samples per minute per series; 15s scrape = 4 DPM | `rate(prometheus_tsdb_head_samples_appended_total[5m]) * 60` |
| GB ingested (logs, traces) | uncompressed bytes received | collector/agent sent-bytes metrics |
| GB retained / queried | storage beyond included retention; bytes scanned | backend usage dashboards |
| Hosts / containers | per-agent or per-node pricing, often with included custom metrics | node count |
| Indexed spans / events | spans kept after retention filters | exporter sent spans after sampling |

## Model
1. Inventory current volume per unit for 30 days; use p95 not average where the vendor does.
2. Apply growth (services, traffic) for 12 months.
3. Price with included allowances and overage rates; add retention extensions and query fees.
4. Sensitivity: what if cardinality doubles, scrape interval halves, log volume +50%.
5. Compare to self-hosting: compute + object storage + engineer time (on-call for the stack).

## Levers per unit
- Active series: drop unused metrics, aggregate away labels, adaptive metrics.
- DPM: 60s scrape for slow metrics.
- Log GB: drop debug, sample repetitive lines, route audit logs to cheap storage.
- Spans: tail sampling, attribute pruning.

## Gotchas
- Some vendors count a series as "active" if it received a sample in the billing hour, so churn (pod restarts, deploys) inflates bills: measure churn too.
- Custom metrics in host-based pricing are capped per host; Prometheus-style histograms count every bucket.
- Commit contracts at forecast p50, not p90, and keep usage alerts.

## Verify
- [ ] The model reproduces last month's invoice within 10%.
- [ ] Usage alerts exist at 80% of committed volume per unit.
