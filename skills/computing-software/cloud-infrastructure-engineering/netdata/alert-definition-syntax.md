---
id: computing-software.cloud-infrastructure-engineering.netdata.alert-definition-syntax
name: alert-definition-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, health-d, alarm-template, alert-lines]
level: practitioner
status: docs-checked
description: "Write a Netdata health alert in health.d: alarm versus template, required lines, minimum requirements to leave UNDEFINED, and a worked ram_usage example."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/REFERENCE.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alerts live in `health.d/*.conf` in the config directory: `sudo ./edit-config health.d/ram-usage.conf`. Health is per node, so a fleet alert needs the same file on every node.

- `alarm: NAME` attaches to one chart (`on:` is a chart ID or name).
- `template: NAME` attaches to every chart of a context (`on:` is a context such as `disk.io`).
- Names allow alphanumerics, `.` and `_` only. The alarm/template line must come first; `on` is required.

Optional lines: `class` (Availability, Errors, Latency, Utilization, Workload), `type`, `component`, `lookup`, `calc`, `every`, `warn`, `crit`, `to`, `exec`, `delay`, `repeat`, `options`, `summary`, `info`.

Minimum: at least one of `lookup`, `calc`, `warn`, `crit`. To leave UNDEFINED you need `warn` or `crit`. Without `lookup`, `every` is required (`s`, `m`, `h`, `d`).

```
 alarm: ram_usage
    on: system.ram
lookup: average -1m percentage of used
 units: %
 every: 1m
  warn: $this > 80
  crit: $this > 90
  info: The percentage of RAM being used by the system.
```

Apply: `sudo netdatacli reload-health`.

Gotchas:
- Names with spaces or hyphens need braces, for example `${Has Number}`; plain `$name` breaks the expression.
- `$status` is the alert's current status, compared with constants such as `$WARNING` and `$CRITICAL`.

## Checked

2026-11-04: alarm versus template, name rules, required and optional lines, the UNDEFINED rule, `every` units, `${...}` braces for names with spaces, per-node configuration and the ram_usage example confirmed against the Netdata health REFERENCE page. Removed the claim that `$status` is "not a dimension" (not stated on the page).

Method: documentation only; no commands were run.
