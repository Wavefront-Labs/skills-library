---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-daemonset-agent
name: otel-collector-daemonset-agent
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [daemonset-collector, node-agent-collector, collector-deployment, k8sattributes, kubeletstats, opentelemetry-collector-helm]
level: practitioner
status: docs-checked
description: "Run the OTel Collector as a per-node DaemonSet agent: node-local OTLP via host IP, k8sattributes filtered by node, kubeletstats and filelog, and forwarding to gateways."
sources: ["https://opentelemetry.io/docs/collector/deployment/agent/", "https://opentelemetry.io/docs/platforms/kubernetes/helm/collector/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DaemonSet agent collector

## Helm
```yaml
mode: daemonset
presets:
  kubernetesAttributes: {enabled: true}
  kubeletMetrics: {enabled: true}
  logsCollection: {enabled: true}
ports:
  otlp: {enabled: true, hostPort: 4317}
config:
  exporters:
    otlp/gateway: {endpoint: otel-gateway.observability.svc:4317, tls: {insecure: true}}
  service:
    pipelines:
      traces: {exporters: [otlp/gateway]}
```

## Apps send to the local node
```yaml
env:
  - name: HOST_IP
    valueFrom: {fieldRef: {fieldPath: status.hostIP}}
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: http://$(HOST_IP):4317
```

## k8sattributes on an agent
Filter to the node to avoid every agent watching every pod:
```yaml
processors:
  k8sattributes:
    filter: {node_from_env_var: K8S_NODE_NAME}
    pod_association:
      - sources: [{from: connection}]          # source IP of the sending pod
```
Set `K8S_NODE_NAME` on the agent pod (for example from `spec.nodeName` via the downward API).

## Why an agent tier
Enrichment with node-local metadata, host metrics and logs, offloading SDK exporters quickly (apps hand off to localhost-ish), and batching before the network hop.

## Gotchas
- Agent resource limits must cover log bursts on busy nodes; set `memory_limiter`.

## Verify
- [ ] Spans arrive with `k8s.pod.name`, `k8s.node.name`; each agent's k8s watch count is limited to its node.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Collector Helm chart page and chart README, the Operator/Kubernetes collector component pages and the k8sattributesprocessor README (main, 2026-10).
- Confirmed: `mode: daemonset`, presets `kubernetesAttributes`, `kubeletMetrics`, `logsCollection`, `ports` with `hostPort`, downward-API `status.hostIP`, `node_from_env_var`, `pod_association`.
- Removed (unconfirmed): `otlp-http` port name, `internalTrafficPolicy` alternative, preset sets `K8S_NODE_NAME`, CNI portmap and hostNetwork gotchas.
Method: documentation only; no commands were run.
