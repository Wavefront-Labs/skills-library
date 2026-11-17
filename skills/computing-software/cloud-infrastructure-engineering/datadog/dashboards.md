---
id: computing-software.cloud-infrastructure-engineering.datadog.dashboards
name: dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, dashboards, widgets, timeboards, screenboards]
level: practitioner
status: docs-checked
description: "Build Datadog dashboards with timeseries, query value, top list and heatmap widgets, groups and layouts."
sources: ["https://docs.datadoghq.com/dashboards/", "https://docs.datadoghq.com/dashboards/widgets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboards and widgets
Goal: build a team dashboard that tells a story.

```
1. Dashboard List > New Dashboard
2. Name it and pick a layout: Dashboard (grid), Timeboard (automatic) or Screenboard (free-form)
3. Add Widget > choose type (timeseries, bar chart, table, event stream ...)
4. Select data source, adjust units and timeframe, add custom links or conditional formatting
5. Save and share
```

- Layouts: Dashboards are grid-based (maximum width 12 grid squares); Timeboards are automatic layouts showing one point in time across the whole dashboard, suited to troubleshooting and correlation; Screenboards are free-form.
- Fastest start: clone a dashboard from the preset list, which holds dashboards from your organisation and out-of-the-box templates for installed integrations, then customise widgets.
- Widget data sources include APM traces, events, logs, metrics, RUM and synthetic test data, SLOs and security data.
- Docs use-case pairings: Timeseries for CPU, memory, network, response times and error rates; Top List for the most resource-intensive hosts or services; Hostmap for resource usage across infrastructure; Query Value for KPIs; Monitor Summary and Alert Graph for alert status and history; Event Stream for real-time events; Service Summary and Topology Map for service health and dependencies.
- In a growing dashboard, group widgets into named tabs: in edit mode use the widget share menu and select Move to tab.
- Refresh depends on the time frame: 10 seconds for 1 to 10 minutes, up to 1 hour for a week or longer; publicly shared dashboards refresh every 30 seconds.

Gotcha: a wide time range refreshes only as often as the table in the docs allows, so do not expect real-time updates on a 1 week or longer view.

## Verify
- The saved dashboard loads and each widget shows data for its chosen source and time frame.

## Checked
2026-11-09. Confirmed against the Dashboards and Widgets overview pages (creation steps, three layout types, grid width, preset cloning, tabs, data sources, use-case pairings, refresh table, public refresh). Removed: the JSON dashboard definition and its query strings (not on these pages), the `ordered` and `free` layout names, the statements that JSON export is for Git, that heavy dashboards slow rendering or raise API usage, the RED metrics advice, the SLO-and-monitor-summary-on-every-service advice, and the text-widget, runbook-link and unused-dashboard cleanup advice.
Method: documentation only; no commands were run.
