---
id: computing-software.cloud-infrastructure-engineering.kubernetes.idle-and-abandoned-workloads
name: idle-and-abandoned-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cost-optimisation, idle-workloads, kube-janitor, cleanup, ownership-labels]
level: practitioner
status: docs-checked
description: "Find idle and abandoned workloads (no traffic, near-zero CPU, stale namespaces) with Prometheus queries and ownership labels, and retire them with TTLs."
sources: ["https://github.com/kubernetes/kube-state-metrics/tree/main/docs/metrics", "https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md", "https://codeberg.org/hjacobs/kube-janitor", "https://www.opencost.io/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding idle and abandoned workloads

## Signals (14-day windows)
```promql
# CPU barely used
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{container!=""}[14d])) < 0.005
# no network received
sum by (namespace, pod) (rate(container_network_receive_bytes_total[14d])) < 100
# deployments created more than 90 days ago (KSM creation timestamp; age alone is not idleness)
time() - kube_deployment_created > 90*86400
```
Add your ingress or gateway controller's request-count metric to confirm "no traffic". Roll
pods up to workloads with `kube_pod_owner` and the ReplicaSet-to-Deployment mapping.

## Ownership
Require `owner` or `team` labels on namespaces (admission policy). Idle workloads without an
owner label are the first candidates; with one, open a ticket to the owner.

## Retire safely
1. Scale to zero, keep objects: `kubectl scale deploy -n <ns> --all --replicas=0`; annotate with
   date and reason.
2. Wait a notice period (two to four weeks).
3. Delete; snapshot PVCs before removing them.

## TTLs for temporary things
kube-janitor deletes objects after a TTL annotation (or at an absolute `janitor/expires` time):
```yaml
metadata:
  annotations:
    janitor/ttl: "7d"
```
Use for preview environments, load-test namespaces and experiments.

## Cost view
OpenCost or Kubecost idle and efficiency reports show money per namespace; pair high-cost and
low-usage to prioritise.

## Verify
The list shrinks month over month and no team reports a surprise deletion (because each step
was announced).

## Checked
2026-10-27 against kube-state-metrics docs (main), the kube-janitor README on Codeberg, the
Kubernetes `kubectl scale` reference (kubernetes/website main, v1.38 development tree; v1.37 is
the latest release) and the OpenCost docs. Confirmed: `kube_deployment_created` is the creation
timestamp and `kube_pod_owner` exists; the cAdvisor metric names (google/cadvisor Prometheus
metrics doc); the
`janitor/ttl` and `janitor/expires` annotations; `kubectl scale --all`. Corrected the claim that
`kube_deployment_created` shows "untouched" deployments, and removed an ingress-nginx metric query
that was not checked.
Method: documentation only; no commands were run.
