---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-cloud-dns-and-additional-pod-ranges
name: gke-cloud-dns-and-additional-pod-ranges
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, cloud-dns-for-gke, kube-dns, nodelocal-dnscache, pod-cidr-expansion, additional-pod-ranges, ip-exhaustion]
level: advanced
status: docs-checked
description: "Move GKE cluster DNS from kube-dns to Cloud DNS (cluster or VPC scope) with NodeLocal DNSCache, and fix pod IP exhaustion by adding discontiguous pod ranges."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/cloud-dns", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/nodelocal-dns-cache", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-pod-cidr", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/flexible-pod-cidr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE Cloud DNS and additional pod ranges

## 1. Cloud DNS for GKE
Cloud DNS for GKE serves cluster DNS from Cloud DNS instead of in-cluster kube-dns pods.
```bash
gcloud container clusters update <C> --region=<R> --cluster-dns=clouddns --cluster-dns-scope=cluster
# then every node pool must be re-created to use Cloud DNS: create a new node pool, or upgrade the pool to a NEW version
# (upgrading a node pool to its current version has no effect on Pods)
```
| Scope | Effect |
|---|---|
| `cluster` | the default scope; names resolvable only inside the cluster (like kube-dns) |
| `vpc` | resolvable from the VPC too (set `--cluster-dns-domain`); not supported on Autopilot; migrating to it is disruptive |
The scope cannot be changed after it is set with `--cluster-dns-scope`. New Autopilot clusters on 1.25.9-gke.400, 1.26.4-gke.500 or later default to Cloud DNS cluster scope, and NodeLocal DNSCache is on by default there. On Standard enable it with:
`gcloud container clusters update <C> --location=<R> --update-addons=NodeLocalDNS=ENABLED` (recreates nodes, which can disrupt workloads).

## 2. Pod IP exhaustion
Each node reserves a pod CIDR sized by max pods per node (up to 110 pods per node on Standard uses a /24; 33-64 uses a /25; 17-32 uses a /26). Symptom: the autoscaler cannot add nodes because the pod range is exhausted.
```bash
# 1) add a secondary range to the subnet
gcloud compute networks subnets update gke-subnet --region=<R> --add-secondary-ranges=pods-2=10.64.0.0/16
# 2a) add it to the cluster (Standard, or Autopilot on 1.26+); it is available to NEW node pools only
gcloud container clusters update <C> --region=<R> --additional-pod-ipv4-ranges=pods-2
# 2b) or pin a new Standard node pool to a user-managed range
gcloud container node-pools create pool-b --cluster=<C> --region=<R> --pod-ipv4-range=pods-2
# (--create-pod-ipv4-range=name=<N>,range=<CIDR> lets GKE create the range; a smaller per-node block comes from --max-pods-per-node)
```
Existing node pools do not pick up new ranges; create a new node pool and move workloads to it. Routes-based clusters do not support additional pod ranges.

## Gotchas
- Firewall rules and Cloud NAT config that list the old pod range must include new ranges (`--nat-custom-subnet-ip-ranges=<SUBNET>:<RANGE_NAME>` includes only that secondary range).
- DNS queries from Pods under Cloud DNS for GKE are billed at Cloud DNS pricing.
- Lower `max-pods-per-node` saves IPs but caps pod density; DaemonSets count towards it.
- Switching cluster DNS on Standard requires re-creating all node pools; schedule it like an upgrade.

## Verify
- [ ] A Pod can resolve `kubernetes.default` after the node pools are re-created; `/etc/resolv.conf` shows `169.254.20.10` when NodeLocal DNSCache is on.
- [ ] Nodes in the new pool get pod CIDRs from `pods-2`.

## Checked

2026-10-24, GKE Cloud DNS, NodeLocal DNSCache, additional Pod IPv4 range and flexible Pod CIDR pages on docs.cloud.google.com, plus the Cloud NAT gcloud reference. Confirmed: `--cluster-dns`, `--cluster-dns-scope` values, `--cluster-dns-domain`, node re-creation requirement, Autopilot defaults, NodeLocalDNS enable command, `--additional-pod-ipv4-ranges`, `--pod-ipv4-range`, `--create-pod-ipv4-range`, pods-per-node to CIDR table, billing note. Corrected: the node pool upgrade to the current version does not apply Cloud DNS (a new version or a new pool is needed), and additional cluster ranges apply to new node pools only. Removed unconfirmed event names and describe format expression.

Method: documentation only; no commands were run.
