---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-slo-setup-and-burn-alerts
name: grafana-slo-setup-and-burn-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-slo, grafana-slo-ratio-query, grafana-slo-threshold-query, grafana-slo-burn-alerts, fast-burn-slow-burn, grafana-slo-terraform, slo-api, grafana-slo-dashboard, slo-report-grafana]
level: practitioner
status: docs-checked
description: "Create Grafana SLOs from ratio or advanced queries, set window, target and fast/slow burn alerts, and know what resources the SLO generates."
sources: ["https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/create/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/introduction/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana SLO

## Create (Alerts & IRM -> SLO -> Create SLO)
Steps: time window, SLI, target and error budget, name and description, alert rules, review and save.
- **Window**: minimum 7 days, default 28 days (a consistent number of weekends).
- **SLI**: a query returning a success ratio between 0 and 1.
  - **Ratio query**: a success metric and a total metric from Prometheus counters; generates the full query with fallbacks.
  - **Advanced query**: custom PromQL (builder or manual), expressed as numerator / denominator.
- **Data sources**: the SLI runs on a source data source (Mimir, Prometheus-compatible, Splunk, AppDynamics, Graphite); recording rules go to a target data source that is Mimir or Prometheus-compatible and accepts recording rules. They may be the same. Multi-stack data sources are not supported. In Terraform the target is `destination_datasource`.
- **Target**: a percentage such as 99%, 98%, 95%. Error budget = 100% - target (99.5% leaves 0.5%). After you enter a target, Grafana SLO simulates outcomes from 90 days of history and shows the probability of meeting it. Avoid a 100% target.
- **Labels**: add team or service labels for ownership; they can route SLO alert notifications.

## Alerts
Two types of burn-rate alert rules:
- **Fast burn**: short evaluation periods; budget would be consumed over minutes or hours (outages, hardware failure).
- **Slow burn**: longer periods; budget would be consumed over hours or days (ongoing issues).
- Per rule you can edit name and description, add labels for routing and annotations (such as runbooks), set the minimum failure threshold, and enable an assistant investigation.
- Alert rules are created only when you save the SLO. By default they are Grafana-managed; the alerting system can be switched in the SLO plugin configuration (Administration > Plugins and data > Plugins), which moves only alert rules, not recording rules. Configure notification policies and contact points in the new system first.
- Burn rate 1 exhausts the budget exactly at the end of the window; 2 exhausts it in half the window (99.9% target with 0.2% error rate gives a burn rate of 2).

## Generated resources
On save Grafana generates, in the SLO's folder: an SLO dashboard (SLI performance and budget consumption), recording rules (10 to 12 per SLO), and optionally alert rules. Deleted resources are recreated automatically. Default limit is 70 SLOs per instance.

## Legacy check
Query `/api/plugins/grafana-slo-app/resources/v1/config`: `{"usesDatasourceRecordingRules": true}` means legacy data source-managed recording rules (needs a Mimir data source with the Ruler API and scopes `metrics:read`, `rules:read`, `rules:write`).

## Checked
2026-11-08. Confirmed in the Grafana SLO landing, Create SLOs and Introduction pages. Removed: the threshold (latency) query type, the Terraform resource example and the SLO HTTP API path (the Terraform registry page returned no readable content and the docs read do not document them), the `grafana_slo_*` series names and SLO report details, the multiwindow multi-burn-rate claim, and the Verify checklist.
Method: documentation only; no commands were run.
