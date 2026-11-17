---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-egress-selector-mode
name: k3s-egress-selector-mode
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, egress-selector-mode, agent-tunnel, agentless-server]
level: sme
status: docs-checked
description: "Choose how the K3s apiserver reaches kubelets and service endpoints with --egress-selector-mode: disabled, agent, pod or cluster."
sources:
  - https://docs.k3s.io/networking/basic-network-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
K3s agents and servers keep websocket tunnels between nodes so the apiserver can reach kubelet and containerd streaming without those ports being exposed to incoming connections. This is equivalent to Konnectivity elsewhere and is configured through the apiserver egress selector.

Set on servers with `--egress-selector-mode` (default agent). Modes:

- disabled: no tunnels to kubelets or cluster endpoints. Servers must run the kubelet, CNI and kube-proxy and have direct connectivity to agents, or the apiserver cannot reach service endpoints or do `kubectl exec` and `kubectl logs`.
- agent (default): tunnels to kubelets. Servers must also run the kubelet, CNI and kube-proxy, or service endpoints are unreachable.
- pod: tunnels to kubelets and service endpoints, routing endpoint connections to the right agent by watching Nodes and Endpoints. Does not work with a CNI that does its own IPAM and ignores the node PodCIDR; use cluster or agent for those.
- cluster: tunnels to kubelets and endpoints, routing by watching Pods and Endpoints. Most portable across configurations, at the cost of more overhead.

The docs recommend pod or cluster when running agentless servers, so the apiserver can reach service endpoints without Flannel and kube-proxy.

## Checked

2026-11-08: read the whole Basic Network Options page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/networking/basic-network-options). Confirmed the tunnel description, default mode and all four mode behaviours. Removed unsupported claims: that the setting must match on all servers, and the --disable-agent flag name.

Method: documentation only; no commands were run.
