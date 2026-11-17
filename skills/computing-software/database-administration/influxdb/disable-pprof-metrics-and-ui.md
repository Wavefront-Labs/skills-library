---
id: computing-software.database-administration.influxdb.disable-pprof-metrics-and-ui
name: disable-pprof-metrics-and-ui
category: computing-software
field: database-administration
product: influxdb
tags: [security, pprof-disabled, metrics-disabled, ui-disabled, production]
level: intro
status: docs-checked
description: "Reduce exposed surface in production by disabling /debug/pprof, /metrics and the bundled UI with three influxd options."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/security/disable-devel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default InfluxDB enables functionality that exposes some information about your instance: two observability endpoints and the bundled UI. Depending on site requirements you may want to disable one or more of them in production. The docs list three configuration options:

- `pprof-disabled`: disables `/debug/pprof`, which provides runtime profiling data.
- `metrics-disabled`: disables `/metrics`, which exposes internal InfluxDB metrics.
- `ui-disabled`: disables the user interface.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): the three options and what each disables. Removed the flag and environment variable spellings, the Prometheus scraping remark and the pointer to a profiling skill, none of which the page states.
Method: documentation only; no commands were run.
