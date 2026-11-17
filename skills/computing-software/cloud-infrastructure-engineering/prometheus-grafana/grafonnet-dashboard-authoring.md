---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafonnet-dashboard-authoring
name: grafonnet-dashboard-authoring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafonnet, grafonnet-dashboard-authoring, grafonnet-panels, jsonnet, dashboards-as-code, grafana]
level: advanced
status: docs-checked
description: "Author Grafana dashboards in jsonnet with the generated grafonnet library: install, variables, time series panels, Prometheus queries, grid helpers."
sources: ["https://grafana.github.io/grafonnet/", "https://github.com/grafana/grafonnet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authoring dashboards with grafonnet

Grafonnet is generated from OpenAPI documents in grafana-foundation-sdk, so it keeps up with Grafana. It is the successor
of the hand-written, builder-pattern grafonnet-lib, which was slow for many dashboards. The project labels itself
experimental, without support or SLAs, and not meant for production use. Use go-jsonnet, not the C implementation,
which has a significant performance issue. Install with jsonnet-bundler:
```bash
jb install github.com/grafana/grafonnet/gen/grafonnet-latest@main
jsonnet -J vendor dashboard.jsonnet
```

## Example
Function names below were checked against the repository's API docs (docs/API).
```jsonnet
local g = import 'github.com/grafana/grafonnet/gen/grafonnet-latest/main.libsonnet';
local var = g.dashboard.variable;
local ts = g.panel.timeSeries;
local prom = g.query.prometheus;

local ds = var.datasource.new('datasource', 'prometheus');
local job = var.query.new('job', 'label_values(up, job)')
            + var.query.withDatasourceFromVariable(ds)
            + var.query.refresh.onTime()
            + var.query.selectionOptions.withMulti();

local rps(title, expr) =
  ts.new(title)
  + ts.queryOptions.withTargets([prom.new('$' + ds.name, expr) + prom.withLegendFormat('{{job}}')])
  + ts.standardOptions.withUnit('reqps')
  + ts.fieldConfig.defaults.custom.withFillOpacity(10);

g.dashboard.new('API overview')
+ g.dashboard.withUid('api-overview')
+ g.dashboard.withTags(['api'])
+ g.dashboard.withVariables([ds, job])
+ g.dashboard.withPanels(
  g.util.grid.makeGrid([
    g.panel.row.new('Traffic'),
    rps('Requests', 'sum by (job) (rate(http_requests_total{job=~"$job"}[$__rate_interval]))'),
  ], panelWidth=12))
```

## Layout helpers
`g.util.grid.makeGrid(panels, panelWidth, panelHeight, startY)` arranges panels in equal-width columns over Grafana's
24-column grid; a `panelWidth` that does not divide 24 leaves a gap on the right. `wrapPanels` wraps to the next row
when the total width exceeds 24, and keeps a panel's own size when it already has one.

## Practices
- Set a fixed uid with `withUid` so links stay stable.
- Put house-style helpers (like `rps`) in a shared lib so dashboards stay short.
- Prefer the grid helpers over hand-placing panels.

## Verify
- [ ] The rendered JSON imports into Grafana and panels show data.

## Checked

2026-11-08. Confirmed against the grafonnet site and README plus the repository's generated API docs for dashboard,
variable, timeSeries, prometheus query, row and util (function names and signatures). Removed as unconfirmed: the
`ts.gridPos` calls (no such field found in the timeSeries docs), `allowUiUpdates` provisioning advice, and the grizzly
and `jsonnetfmt` CI steps.
Method: documentation only; no commands were run.
