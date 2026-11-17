---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.writing-a-monitoring-mixin
name: writing-a-monitoring-mixin
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [writing-a-mixin, mixin-authoring, monitoring-mixins, jsonnet, grafonnet, alerting-rules]
level: advanced
status: docs-checked
description: "Author a monitoring mixin: _config selectors, prometheusAlerts/prometheusRules/grafanaDashboards objects, alert style guide, mixtool lint."
sources: ["https://monitoring.mixins.dev/", "https://github.com/monitoring-mixins/mixtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a monitoring mixin

A mixin is a set of Grafana dashboards and Prometheus rules and alerts packaged as a reusable, extensible jsonnet bundle,
normally installed with jsonnet-bundler. Consumers adapt it by overriding `_config` selectors.

## Shape
Mixins expose three top-level objects, which the consumer examples in the docs read: `prometheusAlerts`,
`prometheusRules` and `grafanaDashboards`, plus the `_config` object. The file layout below is illustrative; the docs
do not prescribe one.
```
myapp-mixin/
  mixin.libsonnet        # imports the pieces
  config.libsonnet
  alerts.libsonnet
  jsonnetfile.json
```
```jsonnet
// config.libsonnet
{ _config+:: { myappSelector: 'job="myapp"' } }
// alerts.libsonnet
{
  prometheusAlerts+:: {
    groups+: [{
      name: 'myapp',
      rules: [{
        alert: 'MyAppHighErrorRate',
        expr: |||
          sum(rate(myapp_requests_total{%(myappSelector)s, code=~"5.."}[5m]))
          / sum(rate(myapp_requests_total{%(myappSelector)s}[5m])) > 0.05
        ||| % $._config,
        'for': '10m',
        labels: { severity: 'warning' },
        annotations: {
          summary: 'MyApp error ratio is high.',
          description: 'MyApp error ratio is {{ printf "%.2f" $value }}.',
        },
      }],
    }],
  },
}
```
Dashboards go in `grafanaDashboards+:: { 'myapp-overview.json': <dashboard> }`.

## Alert style guide (from the docs)
- Name: camel case, no whitespace, capital first letter, with a first component shared by all alerts of the mixin
  (for example NodeFilesystemAlmostOutOfFiles).
- `severity` label: `critical` (immediate action, usually pages), `warning` (action eventually, ticket queue), `info`
  (out of the ordinary, usually not routed).
- Mandatory annotations: `summary` (readable headline, a sentence starting with a capital and ending with a period,
  the same string for alerts grouped in one notification) and `description` (per-alert detail with templated values).
- The docs say `runbook_url` and `dashboard_url` annotations are planned recommendations, not yet standardised.

## Lint and generate with mixtool (alpha-stage)
```bash
mixtool new prometheus-alerts > my-alerts.jsonnet     # also: prometheus-rules, grafana-dashboard
mixtool lint mixin.libsonnet                          # --grafana=false or --prometheus=false skip a half; -J adds vendor paths
mixtool generate all ...                              # subcommands: alerts, rules, dashboards, all
```
The mixtool README warns flags and behaviour may change. Check the options for `generate` with mixtool's own help.

## Consumer override (docs example)
```jsonnet
local kubernetes = import "kubernetes-mixin/mixin.libsonnet";
kubernetes { _config+:: { kubeletSelector: 'job="kubernetes-kubelet"' } }
```
Render with `jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusAlerts)'`.

## Verify
- [ ] A consumer can import the mixin and change only `_config+::` selectors to get working rules.

## Checked

2026-11-08. Confirmed against monitoring.mixins.dev (what a mixin is, consumer override, alert style guide) and the
mixtool README (commands and lint flags; `generate` flags not shown there). The monitoring-mixins/docs repository was
unreachable (504) and was dropped. Removed as unconfirmed: the mandatory directory layout, `promtool test` step,
the `generate all` flag line, and the rule that alerts must carry `runbook_url`.
Method: documentation only; no commands were run.
