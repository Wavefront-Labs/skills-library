---
id: computing-software.database-administration.cloudnative-pg.quickstart-prometheus-grafana-local
name: quickstart-prometheus-grafana-local
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [quickstart, prometheus, grafana, podmonitor, helm, kube-prometheus-stack, alerts]
level: intro
status: docs-checked
description: "Try CloudNativePG monitoring locally: kube-prometheus-stack with sample values, a PodMonitor, default alert rules and the Grafana dashboard."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Part 4 of the Quickstart shows a local observability stack; installing Prometheus and Grafana is outside the project's scope and the steps are for experimentation only.

```sh
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm upgrade --install \
  -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/docs/src/samples/monitoring/kube-stack-config.yaml \
  prometheus-community \
  prometheus-community/kube-prometheus-stack
```

The sample values make the Prometheus Operator watch **any** `PodMonitor`, with Alert Manager and Grafana enabled. A cluster is then scraped by creating a `PodMonitor` that selects `cnpg.io/cluster: cluster-with-metrics` and the `metrics` port:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: cluster-with-metrics
spec:
  selector:
    matchLabels:
      cnpg.io/cluster: cluster-with-metrics
  podMetricsEndpoints:
  - port: metrics
```

Reach Prometheus with `kubectl port-forward svc/prometheus-community-kube-prometheus 9090`. Default alerts come from `kubectl apply -f` the `samples/monitoring/prometheusrule.yaml` file, giving a `cnpg-default-alerts` rule set.

Grafana: `kubectl port-forward svc/prometheus-community-grafana 3000:80`, log in with `admin` / `prom-operator`, then import `grafana-dashboard.json` from the `cloudnative-pg/grafana-dashboards` repository. Panels using the alpha `kubelet_volume_stats_*` metrics may show No data.

## Checked

2026-11-08. Read in full: docs/src/quickstart.md. Helm commands, PodMonitor manifest, port-forward targets and default Grafana credentials confirmed on the Quickstart page (Part 4), which marks the setup experimental only.

Method: documentation only; no commands were run.
