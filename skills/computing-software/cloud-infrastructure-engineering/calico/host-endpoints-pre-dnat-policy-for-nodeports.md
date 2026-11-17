---
id: computing-software.cloud-infrastructure-engineering.calico.host-endpoints-pre-dnat-policy-for-nodeports
name: host-endpoints-pre-dnat-policy-for-nodeports
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [pre-dnat, host-endpoint, nodeport, globalnetworkpolicy, kube-proxy, ingress-only]
level: advanced
status: docs-checked
description: "Use preDNAT policy to filter external traffic by original NodePort before kube-proxy DNAT, and its three differences from host policy."
sources:
  - https://docs.tigera.io/calico/latest/reference/host-endpoints/pre-dnat
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Setting `preDNAT: true` on a host endpoint policy applies its rules before DNAT, so you can match a packet's original destination IP and port. The motivating case is NodePorts: external traffic hits a node IP and NodePort, kube-proxy DNATs it to a pod IP and a different port, and a NodePort uniquely identifies a service while an internal port may not.

Three differences from normal host endpoint policy, because it polices traffic arriving from outside:

1. **Ingress only.** No egress rules; return traffic is covered by standard connection tracking.
2. **Applies to everything arriving through the host endpoint**, even if the packet is routed to a local workload on the same host. Normal host endpoint policy is skipped for traffic going to a local workload.
3. **No default drop.** A host endpoint with no matching pre-DNAT policy lets the packet continue, and it is then accepted or dropped by workload policy (local workload) or normal host endpoint policy (otherwise).

So a pre-DNAT policy needs an explicit Deny to block anything, unlike normal host policy, which drops by default once a host endpoint exists.

The fetched reference gives the concept and rules but no YAML, so write the policy with `preDNAT: true`, selecting your host endpoints, with ingress rules only.

## Checked

Read in full on 2026-11-08: the Pre-DNAT policy page. The preDNAT purpose and the three enforcement differences match it. No example YAML appears on that page, and the closing advice on writing the policy was reduced to what the page supports.

Method: documentation only; no commands were run.
