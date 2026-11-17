---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-logs-drilldown-and-patterns
name: grafana-logs-drilldown-and-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [logs-drilldown, loki, explore-logs, patterns, detected-fields, log-volume, grafana-app]
level: practitioner
status: draft
description: "Use Grafana Logs Drilldown to explore Loki without writing LogQL, and enable the patterns and volume features it needs."
sources: ["https://grafana.com/docs/grafana/latest/explore/simplified-exploration/logs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: fast triage by service, level and log pattern.

Requirements
- Loki with `limits_config.volume_enabled: true` (log volume endpoint) and pattern ingestion:
```yaml
pattern_ingester:
  enabled: true
limits_config:
  allow_structured_metadata: true
  volume_enabled: true
```
- Loki data source in Grafana with `service_name` populated (Loki derives it automatically via `discover_service_name` from labels such as app, job or container).
- Grafana Logs Drilldown app (Explore > Logs, formerly Explore Logs) installed or enabled in your version; confirm naming.

Workflow: pick a service from the overview, switch between Logs, Labels, Fields and Patterns tabs. Patterns show clustered line templates with counts and trends; include or exclude a pattern to refine the query. Add the resulting LogQL to a dashboard.

Gotchas
- Without `service_name`, the landing page is empty; fix labels at ingestion.
- Pattern clustering adds ingester memory; size accordingly.
- Detected fields work best with JSON or logfmt lines.
- Versions older than Loki 3.x lack features; check compatibility.

## Verify
Open the app against a data source; the service list shows entries with volume graphs, and the Patterns tab lists templates.
