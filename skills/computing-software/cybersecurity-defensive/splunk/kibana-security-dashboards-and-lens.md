---
id: computing-software.cybersecurity-defensive.splunk.kibana-security-dashboards-and-lens
name: kibana-security-dashboards-and-lens
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [kibana-dashboards, kibana, kibana-lens, elastic-security, data-views, siem-dashboards, dashboards]
level: practitioner
status: draft
description: "Build security dashboards in Kibana with Lens, data views, controls and drilldowns to Discover/Timeline, scoped by space and role for SOC use."
sources: ["https://www.elastic.co/guide/en/kibana/current/dashboard.html", "https://www.elastic.co/guide/en/kibana/current/lens.html", "https://www.elastic.co/guide/en/kibana/current/data-views.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Kibana dashboards and Lens for security

## Foundations
- **Data view** per data family (`logs-endpoint.*`, `logs-*` with ECS). Set the timestamp field;
  add runtime fields only when unavoidable (computed at query time, slow over long ranges).
- Use **spaces** to separate SOC, platform and executive views; grant via roles with
  space-level privileges. Dashboards in the Security space appear in Security > Dashboards.

## Building panels with Lens
- Drag fields; Lens suggests visualisation. Typical SOC panels:
  - Alerts over time by `kibana.alert.severity` (bar, stacked, `.alerts-security.alerts-*`).
  - Top `host.name` / `user.name` by alert count (table, top values 10, "other" off).
  - Authentication failures by `source.geo.country_iso_code` (map or bar).
  - Unique `process.executable` count trend (metric with sparkline).
- Formulas: `count(kql='event.outcome:failure') / count()` for failure ratios.
- Use **ES|QL** panels for queries Lens cannot express (`STATS ... BY` with evals).

## Interactivity
- **Controls** (options list, range slider, time slider) at top: `host.name`, `user.name`,
  `event.dataset`. Chain controls so selections narrow the next.
- Panel drilldowns: dashboard-to-dashboard (pass filters), or URL drilldown to Timeline/Discover with
  the clicked value.

## Operating
- Save as code: export saved objects (`POST /api/saved_objects/_export`) into git; import with
  overwrite in other spaces/clusters.
- Prefer `.alerts-security.alerts-*` panels over raw-event panels for executive views; raw-event
  aggregations over 30 days are expensive.

## Gotchas
- Mismatched field types across indices (keyword vs text) make fields unaggregatable; fix mappings.
- Time zone defaults to browser; set `dateFormat:tz` for shared screens.

## Verify
Open the dashboard as a SOC-role user in the target space; every panel loads within your SLA (e.g.
under 10 s for 24 h) and controls filter all panels.
