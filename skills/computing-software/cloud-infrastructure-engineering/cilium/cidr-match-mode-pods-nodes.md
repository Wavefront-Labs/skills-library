---
id: computing-software.cloud-infrastructure-engineering.cilium.cidr-match-mode-pods-nodes
name: cidr-match-mode-pods-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, policy-cidr-match-mode, ipblock, networkpolicy, self-hosted-apiserver, beta]
level: advanced
status: docs-checked
description: "Let CIDR and ipBlock selectors match in-cluster pods or nodes with policy-cidr-match-mode, and the identity-allocation cost."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# policy-cidr-match-mode

Beta. By default CIDR selectors do not match in-cluster pods or nodes. Set `--policy-cidr-match-mode=pods` or `=nodes` (Helm `policyCIDRMatchMode: pods` or `nodes`) to allow it.

Caution from the page: leaving it disabled is recommended for most deployments. `pods` allocates extra security identities for every pod matching a CIDR selector, which hurts with many pods, high churn or large CIDR rule sets. Enable only if you must match intra-cluster pod IPs, know your identity limits, and will monitor and revert.

`nodes`: every agent allocates a distinct local identity for all other nodes, about 1 MB extra memory per 1000 nodes. Useful for self-hosted clusters where the apiserver is on in-cluster nodes: normally you need the `kube-apiserver` entity in a CiliumNetworkPolicy, but `nodes` mode lets a Kubernetes NetworkPolicy select the apiserver with an `ipBlock` peer.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
