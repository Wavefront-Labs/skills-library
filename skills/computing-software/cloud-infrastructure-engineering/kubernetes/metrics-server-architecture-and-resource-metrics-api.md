---
id: computing-software.cloud-infrastructure-engineering.kubernetes.metrics-server-architecture-and-resource-metrics-api
name: metrics-server-architecture-and-resource-metrics-api
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metrics-server, resource-metrics-api, kubectl-top, hpa, kubelet-summary-api, horizontal-pod-autoscaler, metrics.k8s.io, aggregated-api, apiservice, observability, monitoring, metrics-server-troubleshooting, kubelet-insecure-tls, metrics-k8s-io]
level: advanced
status: docs-checked
description: "How metrics-server polls kubelet /stats/summary and serves metrics.k8s.io for kubectl top and HPA, and why it cannot replace Prometheus."
sources: ["https://github.com/kubernetes-sigs/metrics-server#readme", "https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#algorithm-details", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/top/top_node.go"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# metrics-server: the resource metrics API, not a monitoring system

**Goal:** know exactly what metrics-server is for (point-in-time CPU/memory for `kubectl top`
and HPA), what it is not (no history, no custom metrics, no alerting), and how to diagnose it
when `kubectl top` returns nothing or HPA stalls at "unknown".

## 1. What it actually does
metrics-server is a single Deployment that:
1. Discovers nodes via the apiserver, then queries each kubelet directly: the
   `/metrics/resource` endpoint from metrics-server v0.6.0 on, the Summary API `/stats/summary`
   in older versions.
2. Keeps per-pod and per-node CPU/memory in an in-memory cache and answers Metrics API requests
   from it. The project says it is meant only for autoscaling and not as a source of monitoring
   data. The shipped manifests set `--metric-resolution=15s`. There is no time series and no
   retention.
3. Registers **APIServices** for `metrics.k8s.io` (the shipped manifests create both
   `v1.metrics.k8s.io` and `v1beta1.metrics.k8s.io`) so the main apiserver proxies `kubectl top`
   and HPA controller requests to it. This is why `kubectl get --raw
   /apis/metrics.k8s.io/v1/nodes` is the first diagnostic command, not a metrics query language.

Two numbers only: CPU (a rate over a cumulative kernel counter; the `window` field in the Metrics
API shows the time window) and memory (working set — see
`computing-software.cloud-infrastructure-engineering.kubernetes.troubleshooting-crashloops-and-oom`).
Everything else — disk, network, custom app metrics, histograms — is out of scope. That is
Prometheus + kube-state-metrics + cAdvisor territory
(`computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-object-state-and-cardinality`,
`computing-software.cloud-infrastructure-engineering.kubernetes.cadvisor-and-cgroup-container-metrics`).

## 2. Why HPA depends on it (and the failure mode that looks like a stuck autoscaler)
HPA's controller loop queries the metrics API every `--horizontal-pod-autoscaler-sync-period`
(default 15s). If metrics-server has no sample for a pod, or a kubelet call fails, the HPA
records `FailedGetResourceMetric` events:
```
kubectl describe hpa <name>
# Warning  FailedGetResourceMetric ...
```
and `TARGETS` prints `<unknown>/<target>`. Common root causes:
- A new pod has no metric sample yet. For CPU, the HPA also sets aside pods that are not yet ready
  or whose latest sample predates readiness (`--horizontal-pod-autoscaler-initial-readiness-delay`,
  `--horizontal-pod-autoscaler-cpu-initialization-period`).
- Missing `resources.requests.cpu` on the container — CPU-based HPA needs a request to compute
  a percentage; memory-based HPA likewise needs `requests.memory`.
- Kubelet certificate problems: the README requires kubelet certificates signed by the cluster CA,
  or `--kubelet-insecure-tls`, which skips verification of kubelet serving certificates and is
  documented as for testing purposes only.

## 3. Deployment gotchas
- Network requirements (README): the control plane must reach the metrics-server pod on port
  10250, and metrics-server must reach each node's kubelet port (default 10250), so NetworkPolicies
  must allow both. Nodes need webhook authentication and authorization, and the apiserver needs
  the aggregation layer enabled.
- `--kubelet-preferred-address-types` sets the order of node address types used to reach each
  kubelet; the flag default is `Hostname,InternalDNS,InternalIP,ExternalDNS,ExternalIP`, while the
  shipped manifests set `InternalIP,ExternalIP,Hostname`.
- Sizing: the default requests (100m CPU, 200Mi) suit up to 100 nodes; add 1m CPU and 2MiB per
  node beyond that. It is not HA by default: set `replicas` above 1 (HA manifest or Helm chart)
  and add `--enable-aggregator-routing=true` to kube-apiserver so requests are load balanced. A
  metrics-server outage stops every HPA that uses resource metrics.
- `kubectl top pod --containers` breaks down per-container; `kubectl top node` computes
  percentages against **allocatable** by default (`--show-capacity` switches to capacity).

## 4. Diagnostic sequence
```bash
kubectl get apiservice v1.metrics.k8s.io -o yaml   # status.conditions: Available=True?
kubectl get --raw /apis/metrics.k8s.io/v1/nodes
kubectl -n kube-system logs deploy/metrics-server
kubectl top nodes   # if nodes work but pods don't, suspect per-node kubelet reachability
```
If the APIService shows `FailedDiscoveryCheck`, the apiserver cannot reach the
metrics-server Service — check its Service/Endpoints and any egress NetworkPolicy on
kube-system.

## Gotchas
- Confusing metrics-server with the **custom metrics API** (`custom.metrics.k8s.io`, usually
  served by prometheus-adapter) — HPA on anything besides CPU/memory needs that separate
  adapter, not metrics-server.
- `kubectl top` shows the latest cached sample over a time window; do not use it to diagnose a
  transient spike.
- Removing metrics-server (e.g. during a migration) silently breaks every HPA in the cluster
  with no immediate alert unless you specifically alert on `FailedGetResourceMetric` events or
  APIService availability.

## Verify
- [ ] `kubectl get apiservice v1.metrics.k8s.io v1beta1.metrics.k8s.io` shows `Available: True`.
- [ ] `kubectl top pod` and `kubectl top node` return numbers across all node pools.
- [ ] Every HPA target's `TARGETS` column shows a real percentage, not `<unknown>`.
- [ ] An alert exists on repeated `FailedGetResourceMetric` HPA events.

## Checked

Checked 2026-10-24 against the metrics-server README, manifests, chart and source on GitHub (default branch, README compatibility table up to 0.9.x), the Kubernetes resource metrics pipeline page in Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), and the kubectl source.
- Kubelet endpoint: `/metrics/resource` from v0.6.0, `/stats/summary` in older versions (resource metrics pipeline page; client source uses `/metrics/resource`).
- Scrape interval: the shipped deployment manifest passes `--metric-resolution=15s`; APIServices `v1.metrics.k8s.io` and `v1beta1.metrics.k8s.io` are both in the base manifests.
- Requirements, default requests and per-node additions, HA via `replicas` and `--enable-aggregator-routing=true`, `--kubelet-preferred-address-types` defaults, `--kubelet-insecure-tls` wording: README.
- `kubectl top node` uses allocatable by default with `--show-capacity` for capacity (kubectl source);
- `FailedGetResourceMetric` is an event reason in the HPA controller source.

Method: documentation only; no commands were run.
