---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rightsizing-workflow-with-vpa-and-goldilocks
name: rightsizing-workflow-with-vpa-and-goldilocks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rightsizing-workflow, goldilocks, vpa, resource-requests, cost-optimisation, prometheus]
level: practitioner
status: docs-checked
description: "Right-size requests and limits from real usage: VPA recommendations in Off mode, Goldilocks dashboards, PromQL percentiles, and a safe rollout loop per workload."
sources: ["https://github.com/FairwindsOps/goldilocks/blob/master/docs/installation.md", "https://github.com/FairwindsOps/goldilocks/blob/master/docs/faq.md", "https://github.com/FairwindsOps/goldilocks/blob/master/docs/advanced.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Right-sizing workflow (VPA recommendations, Goldilocks)

## 1. Collect usage over a full business cycle
Weekly cycles matter. Sources:
- **Goldilocks**: it needs only the VPA recommender (the full VPA install adds the updater and the
  admission webhook). Install with `helm repo add fairwinds-stable https://charts.fairwinds.com/stable`,
  `kubectl create namespace goldilocks`, then
  `helm install goldilocks --namespace goldilocks fairwinds-stable/goldilocks`;
  label namespaces `goldilocks.fairwinds.com/enabled=true`. It creates VPAs with update mode
  `off` for workloads in those namespaces and shows a dashboard with two recommendation types:
  Guaranteed (target as request and limit) and Burstable (lowerBound as request, upperBound as limit).
- **PromQL** directly (cAdvisor metrics):
```promql
# CPU 95th percentile over 14d per container
quantile_over_time(0.95, (sum by (namespace,pod,container) (rate(container_cpu_usage_seconds_total{container!=""}[5m])))[14d:5m])
# memory max working set over 14d
max_over_time(container_memory_working_set_bytes{container!=""}[14d])
```
- `kubectl describe vpa <name>`: `Target` (recommend), `Lower Bound`, `Upper Bound`.

## 2. Decide per resource
- **CPU request**: a high usage percentile (VPA's default target is the 90th percentile of usage,
  `--target-cpu-percentile`).
- **Memory request**: the maximum working set plus headroom (VPA adds a 15% safety margin by
  default, `--recommendation-margin-fraction`); memory overcommit causes OOM kills and node pressure.
- **CPU limit**: a limit below the request is invalid; decide deliberately whether to set one.
- JVM/Node/Go: align runtime heap settings with the new memory limit.

## 3. Roll out safely
1. Change one workload at a time in git, and reduce in steps rather than all at once.
2. Watch after each change: OOMKilled (`kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}`),
   CPU throttling (`container_cpu_cfs_throttled_periods_total` ratio), latency SLOs.
3. Re-evaluate quarterly or after major releases; VPA `Off` keeps recommending.

## 4. Measure the win
Requested vs used per namespace:
```promql
sum by (namespace) (kube_pod_container_resource_requests{resource="cpu"})
/ sum by (namespace) (rate(container_cpu_usage_seconds_total{container!=""}[1h]))
```
Savings only materialise when the autoscaler removes nodes — check node count afterwards.

## Gotchas
- Recommendations from a quiet period undersize; include peak events (month-end, sales).
- VPA recommendations for pods with HPA on CPU are circular — size from load tests instead.
- Sidecars (istio-proxy) are containers too and get their own recommendation; Goldilocks can
  exclude containers with the label `goldilocks.fairwinds.com/exclude-containers`.

## Verify
- [ ] Request/usage ratio per namespace trending down toward your target headroom; no new OOMKills after changes.

## Checked

Checked 2026-10-24 against the FairwindsOps/goldilocks docs on GitHub (installation.md, faq.md, advanced.md) and the VPA flags.md.
- Install commands, repo URL, namespace creation, `goldilocks.fairwinds.com/enabled=true` label, recommender-only requirement: installation.md.
- Guaranteed vs Burstable recommendation definitions and the default update mode of created VPAs: faq.md and advanced.md; `exclude-containers` label: advanced.md.
- VPA defaults quoted (90th percentile, 15% margin): VPA flags.md.
- PromQL metric names (`container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`, `container_cpu_cfs_throttled_periods_total`, `kube_pod_container_resource_requests`, `kube_pod_container_status_last_terminated_reason`) are the standard cAdvisor and kube-state-metrics names; the queries themselves are examples.

Method: documentation only; no commands were run.
