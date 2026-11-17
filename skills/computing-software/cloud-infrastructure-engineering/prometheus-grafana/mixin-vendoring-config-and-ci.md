---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mixin-vendoring-config-and-ci
name: mixin-vendoring-config-and-ci
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [monitoring-mixins, mixins, jsonnet-bundler-usage, vendoring-mixins, mixin-config-overrides, mixin-selectors, mixtool-generate, mixtool-lint, mixin-ci-pipeline, generated-rules-diff, jsonnet]
level: advanced
status: docs-checked
description: "Consume monitoring mixins: vendor with jsonnet-bundler, override _config selectors, render with jsonnet or mixtool, lint, and check generation in CI."
sources: ["https://monitoring.mixins.dev/", "https://github.com/monitoring-mixins/mixtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendoring, configuring and CI for mixins

## Vendor
Mixins are meant to be vendored into your infrastructure repo with jsonnet-bundler, then built with jsonnet.
```bash
go install github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb@latest   # docs use go get on older Go
jb init
jb install github.com/kubernetes-sigs/kubernetes-mixin
```

## Override config
Mixins typically let you override the selectors used for various jobs to match your Prometheus.
```jsonnet
local kubernetes = import "kubernetes-mixin/mixin.libsonnet";
kubernetes {
  _config+:: {
    kubeStateMetricsSelector: 'job="kube-state-metrics"',
    cadvisorSelector: 'job="kubernetes-cadvisor"',
    nodeExporterSelector: 'job="kubernetes-node-exporter"',
    kubeletSelector: 'job="kubernetes-kubelet"',
  },
}
```
Wrong selectors give empty dashboards and alerts that never fire, so set them first.

## Render
```bash
jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusAlerts)' > alerts.yml
jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusRules)' > rules.yml
jsonnet -J vendor -m dashboards_out -e '(import "mixin.libsonnet").grafanaDashboards'
```
With mixtool: `mixtool generate alerts|rules|dashboards|all` and `mixtool lint mixin.libsonnet`. The lint command takes
`--grafana`, `--prometheus` and `-J`/`--jpath`; mixtool is alpha, so check its own help for generate options.

## CI (suggested, not from the docs)
A pipeline step can run `jb install`, render the outputs as above and run `mixtool lint`, failing on errors.
The mixin docs do not prescribe a CI design; the kubernetes-mixin repository itself runs generation, formatting,
linting and rule tests in CI and pins release tags, so review its changelog when bumping.

## Verify
- [ ] The rendered alerts reference series that exist for your selectors.

## Checked

2026-11-08. Confirmed against monitoring.mixins.dev and the mixtool README (and the kubernetes-mixin README for the
override example and CI description). Removed as unconfirmed: the node-mixin install path, `mixtool generate` output
flags, the commit-lockfile advice, the `git diff --exit-code` and `promtool` CI steps, `yq` usage, the `showMultiCluster`
example in the override and PrometheusRule/ConfigMap packaging. The jsonnet-bundler source returned an error and was dropped.
Method: documentation only; no commands were run.
