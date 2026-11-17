---
id: computing-software.cloud-infrastructure-engineering.metallb.choosing-l2-or-bgp
name: choosing-l2-or-bgp
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, announcement, arp, ndp, bgp, layer2, mode-choice]
level: intro
status: docs-checked
description: "Choose between MetalLB layer 2 (ARP/NDP) and BGP announcement: what each needs, how traffic reaches pods, and the headline trade-offs of each."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/layer2.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/bgp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing L2 or BGP

After allocating an IP, MetalLB must announce it. Modes: ARP (IPv4), NDP (IPv6), or BGP.

| | Layer 2 | BGP |
|---|---|---|
| Needs | any Ethernet network, no special hardware | routers you control that speak BGP |
| Who attracts traffic | one leader node per IP | all nodes peer with routers; routers do ECMP |
| Load balancing | none; failover only | per-connection, by packet hash (needs multipath on routers) |
| Bottleneck | one node's bandwidth per service IP | none stated on the page |
| Main downside | slow failover for buggy clients | active connections break when the backend set changes |

In both modes `kube-proxy` makes the final hop to a pod.

Decide:
- Flat LAN, no routers you control: L2. Setup: `computing-software.cloud-infrastructure-engineering.metallb.l2-advertisement-config`.
- Routers with multipath and a need for true spreading: BGP. Setup: `computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-and-advertisement`.
- Both can announce the same pool (`computing-software.cloud-infrastructure-engineering.metallb.dual-announce-l2-bgp`).

## Checked
2026-11-04. Confirmed against the MetalLB Concepts, "layer 2 mode" and "BGP mode" pages: needs, leader versus all-nodes peering, load-balancing behaviour, single-node bottleneck, gratuitous-packet failover, backend-set resets. The decision bullets are the page's own framing (routers you control, true load balancing).
Method: documentation only; no commands were run.
