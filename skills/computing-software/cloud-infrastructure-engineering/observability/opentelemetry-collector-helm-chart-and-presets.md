---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-collector-helm-chart-and-presets
name: opentelemetry-collector-helm-chart-and-presets
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry-collector-helm, collector-helm-presets, collector-deployment, otel-collector, helm]
level: practitioner
status: docs-checked
description: "Deploy the OTel Collector with the opentelemetry-collector Helm chart: mode, image, presets for logs/k8s metadata/kubelet, config merging and removing default components."
sources: ["https://github.com/open-telemetry/opentelemetry-helm-charts/blob/main/charts/opentelemetry-collector/README.md", "https://github.com/open-telemetry/opentelemetry-helm-charts/blob/main/charts/opentelemetry-collector/values.yaml", "https://github.com/open-telemetry/opentelemetry-helm-charts/blob/main/charts/opentelemetry-collector/UPGRADING.md", "https://opentelemetry.io/docs/platforms/kubernetes/helm/collector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opentelemetry-collector Helm chart and presets

## Install
```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install otel-agent open-telemetry/opentelemetry-collector -n observability -f agent-values.yaml
```
The chart README lists Kubernetes 1.24+ and Helm 4.0+ as prerequisites at the time of this check.

## Agent (DaemonSet) values
```yaml
mode: daemonset                     # required: daemonset | deployment | statefulset
image:
  repository: ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-k8s   # as in the chart README install command
command:
  name: otelcol-k8s                 # the README sets this together with the k8s image
presets:
  logsCollection: {enabled: true, includeCollectorLogs: false}   # file log receiver on /var/log/pods/*/*/*.log
  kubernetesAttributes: {enabled: true, extractAllPodLabels: false}  # k8sattributes processor
  kubeletMetrics: {enabled: true}     # kubeletstats receiver
  hostMetrics: {enabled: true}        # hostmetrics receiver
useGOMEMLIMIT: true
resources: {limits: {cpu: 1, memory: 1Gi}}
config:
  exporters:
    otlp: {endpoint: otel-gateway.observability:4317, tls: {insecure: true}}
  service:
    pipelines:
      traces: {exporters: [otlp]}
      metrics: {exporters: [otlp]}
      logs: {exporters: [otlp]}
```
Gateway: `mode: deployment` with `replicaCount`. `presets.clusterMetrics` needs a collector image that includes the
Kubernetes Cluster receiver (the `k8s` distribution); the README says a single active instance monitors a cluster, and
with several replicas leader election is on by default to prevent duplicate metrics. `presets.kubernetesEvents` needs the
Kubernetes Objects receiver and the README's example runs it as `mode: deployment` with `replicaCount: 1`.

## Config merge rules
Your `config:` is merged with the chart defaults (otlp, prometheus, zipkin and jaeger receivers; debug exporter; logs,
metrics and traces pipelines). Lists are not merged, so a list you set replaces the default. Default components can be
removed with `null`:
```yaml
config:
  receivers: {jaeger: null, zipkin: null, prometheus: null}
  service: {pipelines: {traces: {receivers: [otlp]}}}
```
`ports:` (default entries `otlp`, `otlp-http`, `jaeger-compact`, `jaeger-thrift`, `jaeger-grpc`, `zipkin`, `metrics`) should match
the receivers you keep: disable the entries for receivers you removed. Render with `helm template` and inspect the ConfigMap.

## Other useful values
`hostNetwork`, `extraEnvs`, `extraVolumes`/`extraVolumeMounts`, `podMonitor`/`serviceMonitor` (the `metrics` port is 8888),
`autoscaling`, `podDisruptionBudget`, `priorityClassName`.

## Verify
`kubectl -n observability logs ds/otel-agent` shows the collector started without config errors; the collector's own
metrics are served on port 8888.

## Checked

2026-10-25, against the opentelemetry-collector chart README, `values.yaml` and `UPGRADING.md` on main. Confirmed: `mode` values, preset names and fields (`logsCollection`, `includeCollectorLogs`, `kubernetesAttributes`, `extractAllPodLabels`, `kubeletMetrics`, `hostMetrics`, `clusterMetrics`, `kubernetesEvents`), `useGOMEMLIMIT`, default receivers and ports, `null` removal and non-merging lists, values keys listed under 'Other useful values'. Corrected: the README install command sets the ghcr k8s image and `command.name=otelcol-k8s` (not the Docker Hub image); clusterMetrics uses leader election with several replicas rather than requiring a singleton; Helm 4.0+ is listed as a prerequisite. Removed the 'Everything is ready' log line and the yq pipeline.

Method: documentation only; no commands were run.
