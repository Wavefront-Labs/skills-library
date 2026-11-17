---
id: computing-software.cloud-infrastructure-engineering.netdata.parent-ram-sizing
name: parent-ram-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, parent-sizing, ram-requirements, journal-centralization]
level: advanced
status: docs-checked
description: "Estimate RAM for a Netdata Parent from unique metrics, per-entry costs and caches, and tune memory settings when it also centralizes systemd-journal logs."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/ram-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Children default to about 100-200 MB depending on metric count.

Parent formula from the docs:

```
memory = UNIQUE_METRICS x 16KiB + CONFIGURED_CACHES
```

Default `CONFIGURED_CACHES` is 32 MiB. Get the metric count:

```
curl -s http://localhost:19999/api/v3/info | jq '.agents[0].metrics.collected'
```

Per-entry costs: metric with retention 1 KiB; collected metric 20 KiB; metric with ML model 5 KiB (so 26 KiB per collected metric); node with retention 10 KiB; node currently received 512 KiB; node currently sent 512 KiB (1034 KiB per collected node). One million concurrent series is about 16 GiB.

Parents that also centralize systemd-journal logs:
1. Keep metrics and logs on separate disks.
2. Run under expected load for a few hours, check available memory, then set the page cache in `netdata.conf` to one-third of available memory.
3. Netdata 2.1 options in `[db]`: `dbengine out of memory protection` (default 10% of RAM, capped at 5 GiB; set to memory reserved for journals) and `dbengine use all ram for caches` (default `no`).

## Checked

2026-11-04. Confirmed against the Netdata RAM Utilization page: children range, per-entry table, 26 and 1034 KiB totals, the Database Size formula and 32 MiB default caches, the /api/v3/info query, 16 GiB per million series, and the journal-centralization steps and 2.1 options. Removed the closing Verify line, which the page does not state.

Method: documentation only; no commands were run.
