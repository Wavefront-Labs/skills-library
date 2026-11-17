---
id: computing-software.cybersecurity-defensive.splunk.dashboard-drilldowns-and-tokens
name: dashboard-drilldowns-and-tokens
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, siem-dashboards, drilldown, tokens, set-token, link-to-search, investigation-workflow, dashboard-studio]
level: practitioner
status: draft
description: "Wire dashboard drilldowns and tokens so a click moves an analyst from a summary panel to filtered detail, a search, or another dashboard with context."
sources: ["Splunk Docs - Dashboard Studio (Drilldowns, Setting tokens on click)", "Splunk Docs - Simple XML Reference (drilldown element)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drilldowns and tokens

**Goal:** analysts click from "what" to "which" to "show me the events" without retyping
values, so investigations are faster and less error-prone.

## Dashboard Studio event handlers
Set a token from a clicked row:
```json
"viz_top_hosts": {
  "type": "splunk.table",
  "dataSources": {"primary": "ds_hosts"},
  "eventHandlers": [{"type": "drilldown.setToken",
    "options": {"tokens": [{"token": "sel_host", "key": "row.dest.value"}]}}]
}
```
Use it in a detail search: `index=edr dest="$sel_host$" | table _time user process command_line`.
Give the token a default (`"defaults": {"tokens": {"default": {"sel_host": {"value": "*"}}}}`)
or hide the detail panel until it is set (visibility conditions on the panel).

Other handlers:
- `drilldown.linkToSearch`: open Search with the panel query (good default for analysts).
- `drilldown.linkToDashboard`: pass `form.` tokens to another dashboard
  (`"tokens": [{"token": "form.host", "value": "$row.dest.value$"}]`).
- `drilldown.customUrl`: pivot to an external tool (EDR console, ticketing), URL-encode the value.

## Simple XML equivalent
```xml
<drilldown>
  <set token="sel_host">$row.dest$</set>
</drilldown>
```
Keys: `$click.value$`, `$click.name2$`, `$row.<field>$`, `$earliest$`/`$latest$` for the clicked time bucket.

## Design
- Every summary panel should drill somewhere: a filtered table, then raw events.
- Carry the time range: pass `$global_time.earliest$` so the detail matches the summary.
- For time charts, drill on the clicked bucket's time, not the whole dashboard range.

## Gotchas
- Values with quotes or backslashes break searches; use `|s` token filter (`$sel_host|s$`) to quote safely.
- Field names with dots must be accessed as shown in the result columns; renamed fields change the key.
- A drilldown to an external URL leaks the value into that system's logs: avoid for sensitive fields.

## Verify
- [ ] Clicking each panel produces a correctly filtered result with the same time range.
- [ ] Detail panels show a sensible state before any click.
