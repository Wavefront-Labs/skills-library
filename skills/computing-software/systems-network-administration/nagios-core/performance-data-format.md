---
id: computing-software.systems-network-administration.nagios-core.performance-data-format
name: performance-data-format
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, performance-data, perfdata, serviceperfdata, process-performance-data, latency, execution-time, hostperfdata]
level: practitioner
status: docs-checked
description: "Nagios Core performance data: text|perfdata plugin output split into $SERVICEOUTPUT$ and $SERVICEPERFDATA$, check versus plugin perfdata, and the process_performance_data switch."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/perfdata.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance data

Plugin output: human text, then optionally `|` and metrics.

```
PING ok - Packet loss = 0%, RTA = 0.80 ms | percent_packet_loss=0, rta=0.80
```
Text before the pipe goes to `$HOSTOUTPUT$`/`$SERVICEOUTPUT$`; after it to `$HOSTPERFDATA$`/`$SERVICEPERFDATA$`. Nagios does not parse perfdata, so format limits come from consumers (e.g. PerfParse).

## Two categories
- **Check performance data** (always): `$HOSTEXECUTIONTIME$`, `$SERVICEEXECUTIONTIME$`, `$HOSTLATENCY$`, `$SERVICELATENCY$`.
- **Plugin performance data** (optional, plugin-specific): packet loss, disk, load.

## Enable
`process_performance_data` in `nagios.cfg`, plus the per-object `process_perf_data`. Then choose commands or files: `computing-software.systems-network-administration.nagios-core.performance-data-processing`.

Multi-line output rules: `computing-software.systems-network-administration.nagios-core.plugin-exit-codes-output`.

## Checked

2026-11-04. Confirmed against the Performance Data page (pipe split into output and perfdata macros, check versus plugin performance data and their macros, process_performance_data, Nagios not parsing the format) and the Object Definitions page (process_perf_data on hosts and services). Removed an unconfirmed self-check.

Method: documentation only; no commands were run.
