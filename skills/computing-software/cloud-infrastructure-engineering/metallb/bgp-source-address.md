---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-source-address
name: bgp-source-address
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, sourceaddress, bgppeer, multi-homed, per-node-peer, bgp-session]
level: advanced
status: docs-checked
description: "Force the local source IP of a MetalLB BGP session with sourceAddress on BGPPeer; use only with per-node peers selected by a node selector."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP source address

On hosts with several interfaces or addresses, the TCP/IP stack picks the source IP for outbound connections, including BGP. Override it:

```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: example
  namespace: metallb-system
spec:
  myASN: 64512
  peerASN: 64512
  peerAddress: 172.30.0.3
  peerPort: 179
  sourceAddress: 172.30.0.2
  nodeSelectors:
  - matchLabels:
      kubernetes.io/hostname: node-1
```
The speaker checks that `172.30.0.2` exists on one of the host's interfaces. If it does, it is used as source for the session; if not, default behaviour applies (the kernel chooses).

Warning: use `sourceAddress` only with per-node peers, i.e. peers whose node selectors select a single node. A peer without selectors runs on all speaker nodes, and two nodes should not share the same IP, so one fixed source address across nodes is meaningless.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page, "Configuring the BGP source address": example, local-address check and fallback, and the per-node-peer warning. Removed an invented router/tcpdump verification line.
Method: documentation only; no commands were run.
