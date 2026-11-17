---
id: computing-software.cloud-infrastructure-engineering.metallb.traffic-policies
name: traffic-policies
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, externaltrafficpolicy, cluster, local, source-ip, kube-proxy, anti-affinity]
level: practitioner
status: docs-checked
description: "How externalTrafficPolicy Cluster and Local change MetalLB behaviour in L2 and BGP modes: source IP visibility, which nodes attract traffic and per-pod load imbalance."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External traffic policies

MetalLB honours the Service `externalTrafficPolicy`.

## Layer 2
One node attracts the traffic.
- `Cluster` (default): kube-proxy on that node spreads traffic across all pods (uniform), but hides the source IP, so pods see the leader node as the client.
- `Local`: kube-proxy sends only to pods on the same node; no horizontal flow, so pods see the real source IP. Pods not on the leader receive nothing; they are failover replicas.

## BGP
- `Cluster`: every node attracts traffic, uniform across nodes and pods. Two load balancing layers (router, kube-proxy) can cause inefficient flows (router picks node A, kube-proxy sends to a pod on node B). Source IP is hidden: pods see node IPs.
- `Local`: only nodes running a service pod attract traffic. Most efficient path, real source IP preserved. But each node is one unit of balancing regardless of pod count.

Example of the imbalance with `Local`: 2 pods on node A, 1 on node B gives 50% per node, so 25% to each A pod and 50% to the B pod. With `Cluster` each pod gets about 33%.

Advice: with `Local`, control pod placement (for example node anti-affinity) so an even split across nodes means an even split across pods.

Related: a speaker will not advertise a Service with `externalTrafficPolicy=local` when there are no running endpoints on its node (`computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-not-advertising`).

## Checked

2026-11-04. Confirmed against the MetalLB Usage page (Traffic policies: Layer2 and BGP, Cluster and Local behaviour, the 2-pods-on-A, 1-on-B example with 50%, 25%, 50% and 33%, anti-affinity advice) and the Troubleshooting page (no advertising for local policy without local endpoints). Removed the unsupported jsonpath Check line.

Method: documentation only; no commands were run.
