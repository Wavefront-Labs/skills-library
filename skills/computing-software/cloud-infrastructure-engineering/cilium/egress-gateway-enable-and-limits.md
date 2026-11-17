---
id: computing-software.cloud-infrastructure-engineering.cilium.egress-gateway-enable-and-limits
name: egress-gateway-enable-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, egress-gateway, bpf-masquerade, kube-proxy-replacement, enable-egress-gateway, incompatibilities]
level: advanced
status: docs-checked
description: "Enable Cilium egress gateway with egressGateway.enabled, bpf.masquerade and kubeProxyReplacement, and know its incompatibilities with ClusterMesh, kvstore and CES."
sources:
  - https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable egress gateway and its limits

Egress gateway routes IPv4 and IPv6 pod connections to selected external CIDRs through gateway nodes, SNATed to predictable IPs (useful for legacy firewalls).

## Enable
Helm upgrade with `--reuse-values --set egressGateway.enabled=true --set bpf.masquerade=true --set kubeProxyReplacement=true`. ConfigMap keys: `enable-bpf-masquerade: true`, `enable-egress-gateway: true`, `kube-proxy-replacement: true`. Then `kubectl rollout restart ds cilium -n kube-system` and `kubectl rollout restart deploy cilium-operator -n kube-system`.

## Prerequisites
Interfaces and IPs on gateway nodes must be provisioned by you (for example extra ENIs on AWS/EKS).

## Incompatibilities
- Identity allocation mode `kvstore` unsupported; use `identityAllocationMode: crd` (default for new installs).
- Not compatible with Cluster Mesh: the gateway must be in the same cluster as the pods.
- Not compatible with CiliumEndpointSlice (GitHub issue 24833).

## Gotcha
New pods have a delay before policies apply; early traffic may leave with the pod or node IP and bypass the gateway.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway/. Removed the CNI chaining MTU advice, which this page does not state. 

Method: documentation only; no commands were run.
