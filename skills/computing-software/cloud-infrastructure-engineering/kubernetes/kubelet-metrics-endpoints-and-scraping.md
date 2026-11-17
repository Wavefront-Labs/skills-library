---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-metrics-endpoints-and-scraping
name: kubelet-metrics-endpoints-and-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet-metrics-endpoints, metrics-resource-endpoint, kubelet, cadvisor, prometheus, observability]
level: practitioner
status: docs-checked
description: "Know what each kubelet metrics endpoint serves (/metrics, /metrics/cadvisor, /metrics/resource, /metrics/probes, /stats/summary), how to query them, and scrape them with least RBAC."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/", "https://kubernetes.io/docs/reference/instrumentation/node-metrics/", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://github.com/kubernetes-sigs/metrics-server", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet metrics endpoints

All on the kubelet's authenticated HTTPS port **10250** (`port` default). The unauthenticated read-only
port is disabled by default (`readOnlyPort: 0`); leave it that way.

| Endpoint | Content | Typical consumer |
|---|---|---|
| `/metrics` | kubelet's own health: PLEG latency, pod start duration, runtime op errors, volume stats | Prometheus, node troubleshooting |
| `/metrics/cadvisor` | per-container cgroup metrics: `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`, throttling, network, fs | Prometheus dashboards and alerts |
| `/metrics/resource` | small, cheap CPU/memory set for nodes, pods, containers | metrics-server (HPA, `kubectl top`) |
| `/metrics/probes` | `prober_probe_total` (labels include `probe_type`, `result`, `pod`, `container`) | alerting on flapping probes |
| `/stats/summary` | JSON node and pod summary (the Summary API) | debugging; metrics-server 0.6.x and later read `/metrics/resource` instead |

## Query without SSH
```bash
NODE=worker-1
kubectl get --raw "/api/v1/nodes/$NODE/proxy/metrics/resource" | head
kubectl get --raw "/api/v1/nodes/$NODE/proxy/metrics/probes"
kubectl get --raw "/api/v1/nodes/$NODE/proxy/stats/summary"
kubectl get --raw "/api/v1/nodes/$NODE/proxy/metrics" | grep kubelet_pleg_relist_duration_seconds
```

## RBAC for scrapers
Direct scraping (Prometheus to node:10250) needs:
```yaml
rules:
- apiGroups: [""]
  resources: [nodes/metrics, nodes/stats]
  verbs: [get]
```
The kubelet maps `/metrics/*` to `nodes/metrics` and `/stats/*` to `nodes/stats`; every kubelet
path not in its authorization table maps to `nodes/proxy`, so avoid granting `nodes/proxy` to scrapers.
Scraping via the API server proxy (as `kubectl get --raw` does) needs `nodes/proxy` and
also loads the API server; scrape nodes directly at scale.

The Prometheus Operator's `--kubelet-service=<namespace>/<name>` flag (for example
`kube-system/kubelet`) makes it write the kubelet endpoints into a Service that a ServiceMonitor can target.

## Cardinality and cost
`/metrics/cadvisor` is the largest series source in most clusters. Drop series you do not use with
`metricRelabelings` rather than disabling the endpoint.

## Gotchas
- Without a provided cert the kubelet creates a self-signed serving certificate: either enable
  `serverTLSBootstrap` and approve the serving CSRs, or scrapers must skip verification.
- `metrics-server` needs `/metrics/resource` reachable from its pod; its
  `--kubelet-preferred-address-types` flag sets which node address it uses, and `--kubelet-insecure-tls` skips
  verification (testing only).

## Verify
- [ ] `up{job="kubelet"}` = 1 for every node and every endpoint path.

## Checked

2026-10-26: kubernetes.io system-metrics and node-metrics pages, the kubelet authn/authz page, the generated metrics reference (v1.37 docs, kubernetes/website main 2026-10-25), the kubelet config API source, the metrics-server README and the Prometheus Operator source. Confirmed: endpoint list, port 10250 and read-only port default 0, probe metric name and labels, PLEG metric name, subresource mapping for RBAC, metrics-server flags and endpoint, self-signed serving certificate behaviour. Removed unconfirmed kube-prometheus-stack details, series names and jq pipelines.

Method: documentation only; no commands were run.
