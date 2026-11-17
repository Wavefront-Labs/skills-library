---
id: computing-software.cybersecurity-defensive.splunk.dashboard-studio-dashboards
name: dashboard-studio-dashboards
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, siem-dashboards, dashboard-studio, json-dashboard, data-sources, visualizations, absolute-layout, grid-layout, simple-xml-migration]
level: practitioner
status: draft
description: "Build Splunk Dashboard Studio dashboards in JSON: data sources, layout, inputs and tokens, and migrating Simple XML without losing behaviour."
sources: ["Splunk Docs - Dashboard Studio (Create dashboards, Data sources, Inputs and tokens)", "Splunk Docs - Convert Classic (Simple XML) dashboards to Dashboard Studio"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dashboard Studio dashboards

**Goal:** dashboards that load fast, are version-controlled as JSON, and show an analyst
or manager the one decision they need to make.

## Structure of the definition
A Dashboard Studio dashboard is one JSON object (Edit > Source):
```json
{
  "title": "SOC Overview",
  "dataSources": {
    "ds_notables": {"type": "ds.search", "options": {"query": "`notable` | stats count by urgency",
      "queryParameters": {"earliest": "$global_time.earliest$", "latest": "$global_time.latest$"}}}
  },
  "visualizations": {
    "viz_urgency": {"type": "splunk.column", "dataSources": {"primary": "ds_notables"},
      "title": "Notables by urgency"}
  },
  "inputs": {
    "input_time": {"type": "input.timerange", "options": {"token": "global_time",
      "defaultValue": "-24h@h,now"}}
  },
  "layout": {"type": "grid", "globalInputs": ["input_time"],
    "structure": [{"item": "viz_urgency", "type": "block", "position": {"x": 0, "y": 0, "w": 600, "h": 300}}]},
  "defaults": {}
}
```
- `grid` layout reflows; `absolute` gives pixel control for NOC wall screens and lets you
  place images and shapes.
- Data source types: `ds.search` (inline), `ds.savedSearch` (a scheduled report: best for
  heavy panels), `ds.chain` (post-process a base search), `ds.test` (static sample data).

## Design rules
1. Decide the audience: SOC wall (live status, few panels, large numbers), analyst
   (filters and drilldowns), management (trends and SLAs, weekly).
2. Heavy statistics belong in scheduled saved searches or summary indexes; a dashboard with
   ten raw searches over 30 days re-runs all of them per viewer.
3. Every number gets a comparison (vs last week, vs target) and a unit.
4. Use `dynamic coloring` thresholds on single values for SLA breaches, not decoration.

## Migrating from Simple XML
Use the built-in converter (Clone in Dashboard Studio). Check by hand afterwards:
custom JavaScript/CSS is not supported, `<change>` and `<condition>` input logic needs
rework with token defaults and `ds.chain`, and some drilldown behaviours differ.

## Gotchas
- Tokens referenced but never set make the panel wait forever ("Waiting for input").
- Queries in JSON need escaped quotes; paste through the editor, not by hand.
- Permissions: the dashboard runs searches as the viewer, so restricted users see empty
  panels rather than errors when they lack index access.

## Verify
- [ ] JSON stored in an app in Git and deployed via the deployer, not edited in production.
- [ ] Load time under 10 seconds for the default time range (Job Inspector on each search).
- [ ] Every panel has a stated question it answers.
