---
id: computing-software.cloud-infrastructure-engineering.cilium.ciliumegressgatewaypolicy-authoring
name: ciliumegressgatewaypolicy-authoring
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, ciliumegressgatewaypolicy, egressip, destinationcidrs, excludedcidrs, gateway-node]
level: advanced
status: docs-checked
description: "Write CiliumEgressGatewayPolicy: pod selectors, destinationCIDRs and excludedCIDRs, gateway node selection, egressIP vs interface, multiple gateways."
sources:
  - https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CiliumEgressGatewayPolicy

Cluster-scoped (no namespace). Select namespaces with label `io.kubernetes.pod.namespace` in a selector.

- `selectors[].podSelector` (`matchLabels` or `matchExpressions`), optional `nodeSelector` (cannot be used alone; only security-relevant labels count).
- `destinationCIDRs` (IPv4/IPv6). Internal cluster IPs (pods, nodes, API server) inside them are excluded from SNAT. `excludedCIDRs` carves exceptions.
- `egressGateway.nodeSelector` picks the gateway node; with several matches the first node by lexical name wins. No match: matching traffic is dropped.

## Choosing the egress IP
1. `interface: ethX` uses the first IPv4 and IPv6 on that interface.
2. `egressIP: a.b.c.d` with a per-packet route lookup. The IP must be assigned to a network device on the gateway node.
3. Omit both: default-route interface and its first IPs.
Specify both `egressIP` and `interface` and the policy is IGNORED. Make sure the agent runs on that interface via `--devices`.

If no egress IP can be selected the gateway drops traffic with reason `No Egress IP configured`. Cilium does not react to later IP changes on the node; re-apply the policy to force reselection.

## Multiple gateways
Use `egressGateways` (a list with the same fields). Each source endpoint uses a single gateway chosen by its CiliumEndpoint UID; changes to selectors or matching nodes reassign endpoints and break existing connections (GitHub issue 39245).

Interface for multi-NIC gateways is chosen from `ip route get <externalIP> from <egressIP>`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway/. Removed the local-route and GCE/GKE detail, which the page does not state. 

Method: documentation only; no commands were run.
