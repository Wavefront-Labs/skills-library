---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-mixins-with-jsonnet
name: monitoring-mixins-with-jsonnet
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, grafana, monitoring-mixins, mixins, kube-prometheus-mixin, kubernetes-mixin, node-mixin, jsonnet, jsonnet-bundler, jb, mixtool, grafonnet, prometheus-rules, grafana-dashboards, alerts-as-code, dashboards-as-code, config-overrides, selectors, runbook-url, ci-rules]
level: advanced
status: docs-checked
description: "Consume monitoring mixins: vendor with jsonnet-bundler, override _config selectors, render alerts, rules and dashboards with jsonnet, lint with mixtool."
sources: ["https://monitoring.mixins.dev/", "https://github.com/monitoring-mixins/mixtool", "https://github.com/kubernetes-sigs/kubernetes-mixin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring mixins with jsonnet

A mixin is a set of Grafana dashboards and Prometheus rules and alerts packaged as a reusable, extensible bundle,
written in jsonnet and typically installed and updated with jsonnet-bundler. Mixins are designed to be vendored into
the repo that holds your infrastructure config.

## Consume the kubernetes-mixin
The repository moved to `kubernetes-sigs/kubernetes-mixin`; the old `kubernetes-monitoring` path still redirects.
```bash
jb init
jb install github.com/kubernetes-sigs/kubernetes-mixin
```
```jsonnet
// mixin.libsonnet
local kubernetes = import "kubernetes-mixin/mixin.libsonnet";
kubernetes {
  _config+:: {
    kubeStateMetricsSelector: 'job="kube-state-metrics"',
    cadvisorSelector: 'job="kubernetes-cadvisor"',
    nodeExporterSelector: 'job="kubernetes-node-exporter"',
    kubeletSelector: 'job="kubernetes-kubelet"',
    grafanaK8s+:: { dashboardNamePrefix: 'Mixin / ', dashboardTags: ['kubernetes', 'infrastucture'] },
  },
}
```
Selectors are overridden so they match the jobs in your Prometheus. Render alerts, rules and dashboards:
```bash
jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusAlerts)' > alerts.yml
jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusRules)' > files/rules.yml
jsonnet -J vendor -m files/dashboards -e '(import "mixin.libsonnet").grafanaDashboards'
```
Pass the alerts and rules files to Prometheus and import the dashboard files into Grafana; how depends on your stack.
Other deployment routes in the docs: ksonnet (prometheus-ksonnet) or kube-prometheus.

## kubernetes-mixin specifics (README)
- Mixin versions do not map one-to-one to Kubernetes versions. Pin a release tag (`version-MAJOR.MINOR.PATCH`) and read
  its changelog on upgrade; releases from 1.4.0 and master need Kubernetes v1.29+ scheduler metrics, and the API-server
  rules need `apiserver_request_sli_duration_seconds` (Kubernetes v1.26+).
- Multi-cluster dashboards: opt in with `showMultiCluster: true` and `clusterLabel: '<your cluster label>'`; needs a
  multi-cluster Thanos with `external_labels` or a Cortex system with a cluster label.
- Rules use `$__rate_interval` (Grafana 7.2+); set `grafana72: false` in `_config` for older Grafana.
- Deprecated recording rule `node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate` is slated for
  removal in v2.0.0, replaced by `...:sum_rate5m`.
- `make generate` builds the alerts, rules and dashboards in a checkout; `make test` runs the tests.
- The README suggests `prom-metrics-check` to verify that dashboard metrics exist in your Prometheus.

## Lint
`mixtool lint mixin.libsonnet` checks structure; `--grafana=false` or `--prometheus=false` skip a half and `-J` adds
vendor paths. mixtool is alpha-stage; its flags may change. `mixtool generate` has `alerts`, `rules`, `dashboards`
and `all` subcommands (check its help for options).

## Alert severity convention
critical pages someone immediately; warning goes to a work queue; info marks an out-of-the-ordinary condition that is
not worth a page or ticket.

## Verify
- [ ] Every selector you set returns series in Prometheus, and generated dashboards show data.

## Checked

2026-11-08. Confirmed against monitoring.mixins.dev, the mixtool README and the kubernetes-mixin README. Removed as
unconfirmed: node-mixin install path and its config keys, the alert-group filter example, the `runbookURLPattern`
key, the `mixtool generate all` flag usage, ConfigMap/PrometheusRule delivery steps, and the jsonnetfile.lock and
grafana-dashboard-linter advice. The jsonnet-bundler and mixins design-doc sources returned errors and were dropped.
Method: documentation only; no commands were run.
