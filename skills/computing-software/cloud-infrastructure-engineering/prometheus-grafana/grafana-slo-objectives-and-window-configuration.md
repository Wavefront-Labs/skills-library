---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-slo-objectives-and-window-configuration
name: grafana-slo-objectives-and-window-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-slo, grafana-slo-objective, slo-window-config, error-budget, slo-as-code]
level: practitioner
status: docs-checked
description: "Set objectives and time windows in Grafana Cloud SLO: window, SLI query, target and error budget, generated resources, burn alerts, and best practices."
sources: ["https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/create/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana SLO objectives and windows

**Goal:** an SLO whose target and window match how users judge reliability. Grafana SLO is part of Grafana Cloud.

## Window, SLI, target
- **Time window**: the whole period the SLO is evaluated over. Minimum 7 days; default 28 days, which gives a
  consistent number of weekends and handles weekend traffic variation better than 30 days.
- **SLI**: a query returning the success ratio, a value between 0 and 1 per evaluation period. For all SLO features to
  work it must be expressed as numerator / denominator. Two options: **Ratio query** (success metric and total metric
  from Prometheus counters; Grafana generates the full query with fallbacks) or **Advanced query** (custom, graphical
  builder or manual).
- **Target**: a percentage (99%, 98%, 95%...). The **error budget** is automatically 100% - target; 99.5% leaves 0.5%
  of requests that can fail over the window.
- **Statistical predictions**: after you enter a target Grafana queries 90 days of history of the raw metrics, simulates
  scenarios and shows the probability of meeting the target. It can fail to produce one, in which case the remaining
  error budget panel is shown.

## Data sources
SLI source can be Mimir, Prometheus-compatible data sources, Splunk, AppDynamics or Graphite (multi-stack data sources
are not supported). The target data source, which stores the recording rules, must be Mimir or another
Prometheus-compatible source that accepts recording rules; source and target may be the same. Terraform calls the
target `destination_datasource`.

## What Grafana generates
Placed in the same folder as the SLO: an SLO dashboard (SLI performance and error budget consumption), recording rules,
and optional alert rules. If deleted, Grafana recreates them. Alert rules are only created once the SLO is saved.

## Alerts
- **Fast-burn**: short evaluation periods, fires when the budget is consumed quickly (minutes or hours; outages).
- **Slow-burn**: longer periods, budget consumed gradually (hours or days).
- Options: name, description, labels for routing, annotations such as runbooks, and a minimum failure threshold.
- Default alerting uses Grafana-managed alert rules; data source-managed rules are selectable under the SLO plugin
  configuration, and only alert rules move between systems (stored in Mimir namespace `grafana_slo_<STACK ID>`).
- Suggested practice: route fast-burn to designated engineers via OnCall or your main escalation channel, and slow-burn
  to group notifications in working hours.

## Best practices (from the vendor page)
- Make targets attainable, not aspirational; an SLO is not an OKR. Teams, not managers, should create SLOs and review
  them at regular intervals; adjust objectives if much budget is left over.
- Start with availability and latency; prefer event-based SLIs over time-based; avoid percentile SLIs such as "p95
  under 2s", count all requests meeting the target.
- Very low traffic gives noisy alerts, very high can mask customer-specific issues; supplement low traffic with
  synthetics, or raise Minimum Failures (applies to all alert windows, the smallest being 1 hour).

## Verify
- [ ] The prediction chart and SLI history look consistent with what you remember of recent incidents.
- [ ] Notification policies and contact points exist in whichever alerting system is selected.

## Checked
Checked 2026-11-08 against the Grafana Cloud "Create SLOs" and "Best practices for Grafana SLOs" pages. Removed: the
`grafana_slo_*` metric name claim and "several rates" recording rule detail, the target/window choosing table, the
options list "7d, 14d, 28d, 30d", the 30-90 day measurement advice and the Terraform `grafana_slo` example (registry
page returned no readable content).
Method: documentation only; no commands were run.
