---
id: computing-software.cloud-infrastructure-engineering.kubernetes.coredns-scaling-and-dns-autoscaler
name: coredns-scaling-and-dns-autoscaler
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, coredns, coredns-replicas, dns-autoscaler, cluster-proportional-autoscaler, dns-performance]
level: practitioner
status: docs-checked
description: "Scale CoreDNS with cluster size: cluster-proportional-autoscaler (cores/nodes per replica), anti-affinity and PDB, resources, and the metrics that show DNS saturation."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/dns-horizontal-autoscaling/", "https://github.com/kubernetes-sigs/cluster-proportional-autoscaler", "https://coredns.io/plugins/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CoreDNS scaling and the DNS autoscaler

kubeadm's CoreDNS manifest sets a fixed replica count, a PriorityClass of
`system-cluster-critical`, `maxUnavailable: 1`, requests of `cpu: 100m` and `memory: 70Mi`, a
memory limit of `170Mi` and `lameduck 5s` in the health plugin. At large node counts or with
DNS-heavy apps those defaults saturate, so scale CoreDNS with the cluster.

## DNS horizontal autoscaling (cluster-proportional-autoscaler)
The Kubernetes task page runs the `kube-dns-autoscaler` Deployment, configured by a ConfigMap of
the same name in `kube-system`:
```
linear: '{"coresPerReplica":256,"min":1,"nodesPerReplica":16}'
```
replicas = max( ceil( cores / coresPerReplica ), ceil( nodes / nodesPerReplica ) ), clamped by
`min` and `max`; `coresPerReplica` dominates on clusters with many cores per node and
`nodesPerReplica` dominates on clusters with small nodes. The cluster-proportional-autoscaler
project also publishes a Helm chart (repo
`https://kubernetes-sigs.github.io/cluster-proportional-autoscaler`); its `options.target`
value names the workload to scale and `config.linear` holds the same parameters (check the chart's
`values.yaml`, where `preventSinglePointFailure` and `includeUnschedulableNodes` appear in the
documented linear example).

Do not also attach an HorizontalPodAutoscaler to the same Deployment; two controllers would
set its replica count.

## Make the replicas count
- Spread replicas across nodes and zones (topology spread constraints or pod anti-affinity).
- Keep a PodDisruptionBudget so drains do not remove all replicas.
- Watch CoreDNS memory and CPU against the manifest defaults as the cluster grows, and raise
  them if needed.
- NodeLocal DNSCache is the Kubernetes-documented option for reducing query load on CoreDNS.

## Saturation signals
Use the CoreDNS `metrics` plugin (Prometheus metrics on port 9153 in kubeadm's Corefile):
request rate per pod, request duration histogram and the container's CPU throttling. Throttled
CoreDNS means raise or remove the CPU limit; rising latency with rising query rate means add
replicas.

## Verify
- [ ] After adding nodes the CoreDNS Deployment's replicas follow the configured formula.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the DNS horizontal autoscaling task page (kube-dns-autoscaler, linear ConfigMap format and formula), the cluster-proportional-autoscaler README and chart values (Helm repo URL, options.target, linear parameters) and kubeadm's CoreDNS manifest source (priority class, maxUnavailable, requests, limit, lameduck, prometheus port 9153). Removed the claims about 2 replicas for all sizes, GKE and EKS autoscaler behaviours, the min 2 / max 50 example values, specific PromQL queries and the latency target.

Method: documentation only; no commands were run.
