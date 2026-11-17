---
id: computing-software.cloud-infrastructure-engineering.netdata.override-stock-alerts
name: override-stock-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, override-alert, stock-alerts, chart-id]
level: practitioner
status: docs-checked
description: "Change thresholds of stock Netdata alerts safely: override all instances with a template, one instance with an alarm, or copy the whole stock file."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/overriding-stock-alerts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Never edit the stock directory; updates replace it. Put overrides in `health.d/` under the user config directory (`sudo ./edit-config health.d/my-overrides.conf` resolves the path). User definitions load before stock, so a same-name override wins.

1. All instances: create a template with the same name and context, and change thresholds. The stock template is skipped. If the stock alert is an alarm (rare), override with an alarm.
2. One instance: keep the stock template and add an alarm with the same name and `on:` set to the chart ID (for example `disk_space._mnt_data`). Find IDs:

```
curl -s "http://localhost:19999/api/v1/charts" | grep -o '"id":"disk_space[^"]*"'
```

   For several instances use `chart labels:` in a template.
3. Whole file: `sudo ./edit-config health.d/cpu.conf` makes a user copy; Netdata then loads only that file, so it must contain every alert you need.

Apply: `sudo netdatacli reload-health`.

Verify the `source` field:

```
curl -s "http://localhost:19999/api/v1/alarms?all" | jq '.alarms | to_entries[] | select(.value.name == "20min_steal_cpu") | .value'
```

Gotchas:
- Overrides are full definitions, not patches; omitted fields fall back to defaults.
- A `host labels` scope that the stock alert lacks leaves the stock alert active on hosts your override does not match.
- UI edits create a dynamic config that overrides files until reset.

## Checked

2026-11-04: override methods, chart ID lookup command, whole-file shadowing, full-definition behaviour, the verify command and UI-edit behaviour confirmed against the Netdata overriding-stock-alerts page.

Method: documentation only; no commands were run.
