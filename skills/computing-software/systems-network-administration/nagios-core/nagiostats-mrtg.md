---
id: computing-software.systems-network-administration.nagios-core.nagiostats-mrtg
name: nagiostats-mrtg
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, nagiostats, mrtg, performance-graphs, check-latency, mrtg-cfg, nagios-statistics]
level: practitioner
status: docs-checked
description: "Use nagiostats to read live Nagios Core statistics and feed MRTG (--mrtg --data) to graph check latency, volume, cached and passive counts."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/nagiostats.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/mrtggraphs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nagiostats and MRTG

## nagiostats
Ships with the daemon. Human-readable report:
```
/usr/local/nagios/bin/nagiostats -c /usr/local/nagios/etc/nagios.cfg
```
It prints "CURRENT STATUS DATA": status file age, PID, command and check-result buffer use, host/service state counts, latency and execution times (min/max/avg), active/passive counts for the last 1, 5, 15, 60 minutes, scheduled vs on-demand vs cached checks, external command counts.

`nagiostats --help` lists the valid `--data` values (the page does not enumerate them).

## MRTG
`nagiostats --mrtg --data <value>` emits MRTG-compatible output. Copy the sample entries from `mrtg.cfg` in the distribution's `sample-config/` into `/etc/mrtg/mrtg.cfg`; graphs appear after MRTG's next run.

Sample graphs: active/passive/cached host and service checks, average latency and execution time, state-change volatility, external commands.

## Use
Persistent high latency: tune `max_concurrent_checks`, `check_result_reaper_frequency`, `max_check_result_reaper_time` (`computing-software.systems-network-administration.nagios-core.performance-tuning-tips`).

## Checked

2026-11-04. Read the nagiostats and Graphing With MRTG pages: -c with nagios.cfg gives the CURRENT STATUS DATA report (status file age, PID, command and check result buffers, state counts, latency and execution min/max/avg, last 1/5/15/60 minute counts, scheduled/on-demand/cached checks, external commands), --help lists valid --data values, --mrtg with --data gives MRTG output, sample entries in sample-config/mrtg.cfg copied to /etc/mrtg/mrtg.cfg, and the three tuning variables named for high latency. Nothing removed.

Method: documentation only; no commands were run.
