---
id: computing-software.cybersecurity-defensive.splunk.splunk-dashboard-inputs-and-tokens
name: splunk-dashboard-inputs-and-tokens
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, dashboard-inputs, tokens, time-picker, dashboard-studio, simple-xml, siem-dashboards]
level: practitioner
status: draft
description: "Use Splunk dashboard inputs (time picker, dropdowns, multiselect, text) with tokens, dynamic populating searches, defaults and token prefix/suffix for SOC dashboards."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/DashStudio/inputs", "https://docs.splunk.com/Documentation/Splunk/latest/Viz/FormEditor", "https://docs.splunk.com/Documentation/Splunk/latest/Viz/tokens"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dashboard inputs

## Dashboard Studio (JSON)
```json
"inputs": {
  "input_time": {"type": "input.timerange", "options": {"token": "tr", "defaultValue": "-24h@h,now"}, "title": "Time"},
  "input_host": {"type": "input.multiselect", "title": "Host",
    "options": {"token": "host", "defaultValue": ["*"], "items": [{"label": "All", "value": "*"}]},
    "dataSources": {"primary": "ds_hosts"}}
}
```
- Dynamic items: a data source `| tstats count where index=wineventlog by host | fields host` with
  `"items": ">frame(label, value) | prepend(...)"` or the UI "dynamic" option.
- Use in searches: `index=wineventlog host IN ($host$)` with time `"queryParameters": {"earliest": "$tr.earliest$", "latest": "$tr.latest$"}`.
- Multiselect tokens: set value prefix/suffix and delimiter in Simple XML; in Studio the token is a
  comma list; `IN ($host$)` handles it if values are quoted (`"valuePrefix"`-style formatting via
  `| eval value="\"".host."\""`).

## Simple XML
```xml
<input type="multiselect" token="host">
  <label>Host</label><choice value="*">All</choice><default>*</default>
  <valuePrefix>host="</valuePrefix><valueSuffix>"</valueSuffix><delimiter> OR </delimiter>
  <search><query>| tstats count where index=wineventlog by host</query></search>
  <fieldForLabel>host</fieldForLabel><fieldForValue>host</fieldForValue>
</input>
```
- Text inputs: escape user input; a token inserted raw into SPL lets a user change the search.
  Use `$user|s$` (quoted) filters in Simple XML.
- `searchWhenChanged="false"` plus a Submit button for expensive dashboards.

## Patterns
- Global time picker plus per-panel overrides for "last 7 days baseline".
- Hidden tokens set by drilldowns to reveal detail panels (`depends="$selected_user$"`).

## Gotchas
- Populating searches run on every load; use `tstats` or lookups, never raw event scans.
- Default `*` with `IN` breaks; use `host=*` when "All".
- Tokens unset on load leave panels "waiting for input"; always give defaults.

## Verify
Select each input value including All and empty; every panel's search (open in search) shows the
expected substituted SPL.
