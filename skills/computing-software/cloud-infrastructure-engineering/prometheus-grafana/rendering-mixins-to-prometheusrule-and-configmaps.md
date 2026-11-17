---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.rendering-mixins-to-prometheusrule-and-configmaps
name: rendering-mixins-to-prometheusrule-and-configmaps
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mixin-to-prometheusrule, mixin-rendering, monitoring-mixins, prometheusrule-crd, jsonnet, grafana-dashboards]
level: practitioner
status: draft
description: "Render jsonnet mixins into PrometheusRule objects and Grafana dashboard ConfigMaps (sidecar label) for Kubernetes, with a reproducible build script."
sources: ["https://monitoring.mixins.dev/", "https://github.com/monitoring-mixins/mixtool", "https://github.com/grafana/helm-charts/tree/main/charts/grafana#sidecar-for-dashboards"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rendering mixins to PrometheusRule and ConfigMaps

A mixin exposes `prometheusAlerts`, `prometheusRules` and `grafanaDashboards`. For Kubernetes you wrap them in objects the operator and Grafana sidecar consume.

## build.jsonnet
```jsonnet
local mixin = (import 'kubernetes-mixin/mixin.libsonnet') + {
  _config+:: { cadvisorSelector: 'job="kubelet", metrics_path="/metrics/cadvisor"' },
};
{
  'prometheusrule.json': {
    apiVersion: 'monitoring.coreos.com/v1',
    kind: 'PrometheusRule',
    metadata: { name: 'kubernetes-mixin', namespace: 'monitoring', labels: { release: 'kps' } },
    spec: { groups: mixin.prometheusAlerts.groups + mixin.prometheusRules.groups },
  },
} + {
  ['dashboard-' + std.strReplace(name, '.json', '') + '.json']: {
    apiVersion: 'v1',
    kind: 'ConfigMap',
    metadata: { name: 'dash-' + std.strReplace(name, '.json', ''), namespace: 'monitoring',
                labels: { grafana_dashboard: '1' } },
    data: { [name]: std.manifestJsonEx(mixin.grafanaDashboards[name], '  ') },
  }
  for name in std.objectFields(mixin.grafanaDashboards)
}
```
```bash
jb install                                   # vendor/ from jsonnetfile.json
jsonnet -J vendor -m out/ build.jsonnet      # one file per top-level key
kubectl apply --server-side -f out/
```
Plain Prometheus: `jsonnet -J vendor -S -e 'std.manifestYamlDoc((import "mixin.libsonnet").prometheusAlerts)' > alerts.yml` and `promtool check rules alerts.yml`.

## Notes
- The PrometheusRule needs the labels your Prometheus CR's `ruleSelector` expects.
- Grafana Helm sidecar watches ConfigMaps with `grafana_dashboard` label (configurable); large dashboards can exceed the 1 MiB ConfigMap limit: split or compress via provisioning files instead.
- Commit rendered output so reviews show the real diff.

## Verify
- [ ] `promtool check rules` passes on rendered YAML; rules appear in Prometheus `/rules`; dashboards appear in Grafana folder.
