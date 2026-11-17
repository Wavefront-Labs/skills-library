---
id: computing-software.cloud-infrastructure-engineering.cilium.host-policies
name: host-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, host-policies, ciliumclusterwidenetworkpolicy, node-selector, host-firewall, extended-ip-protocols]
level: advanced
status: docs-checked
description: "Write Cilium host policies with a nodeSelector, enable hostFirewall, allow protocols such as VRRP, and avoid host L7 DNS upgrade pitfalls."
sources:
  - https://docs.cilium.io/en/stable/security/policy/host/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host policies

Host policies are a `CiliumClusterwideNetworkPolicy` with a `nodeSelector` instead of an endpoint selector. L3/L4 rules on ingress and egress plus L7 DNS rules only (beta). They apply to the host namespace, including host-networking pods, not to non-host pods talking outside the cluster.

## Install
Helm flags: `--set hostFirewall.enabled=true` and `--set devices='{eth0}'` (omit devices to auto-detect).

Docs example: nodes labeled `type=ingress-worker` allow TCP 22, 6443, 2379, 4240 and UDP 8472 (VXLAN). Replace ports for your environment.

## Extended protocols
Protocols without ports (VRRP 112, IGMP 2, GRE 47, IPIP 4, IPV6 41, ESP 50, AH 51) are dropped with `DROP_CT_UNKNOWN_PROTO` unless `--enable-extended-ip-protocols` is true.

## Host L7 DNS caution
All host DNS goes through the agent DNS proxy, which is down while the agent restarts, so lookups (including kube-apiserver FQDN for kubelet) time out. Pre-pull the new agent image before upgrades; exempt the Cilium image from image credential verification if `KubeletEnsureSecretPulledImages` is enabled; Kubernetes 1.33 and 1.34 can delay agent restart by minutes. With per-endpoint routes, in-cluster upstream DNS times out.

## Troubleshooting
`kubectl get CiliumClusterwideNetworkPolicy -o yaml`; check node labels; get host endpoint ID `cilium-dbg endpoint get -l reserved:host -o jsonpath='{[0].id}'`; check `PolicyAuditMode` via `cilium-dbg endpoint config $HOST_EP_ID | grep PolicyAuditMode`; `cilium-dbg status list` for Host firewall devices; `cilium-dbg monitor --related-to $HOST_EP_ID`.

## Known issues
Initial enforcement may drop legitimate replies for seconds; unsupported with IPsec and on WireGuard host interfaces; unknown L2 protocols (LLC, VRRP) are dropped; without kube-proxy replacement for NodePort, policies apply to service addresses.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/host/. 

Method: documentation only; no commands were run.
