---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-leader-election
name: l2-leader-election
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, leader-election, brain-split, keepalived, vrrp, layer2, memberlist]
level: advanced
status: docs-checked
description: "How MetalLB L2 picks the announcing node statelessly via hashed node+VIP lists, effects of adding or removing nodes, split-brain risk, and differences from Keepalived/VRRP."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/layer2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 leader election

Each speaker computes the leader for a VIP itself; no state is kept about who is in charge.

1. Each speaker builds the list of potential announcers for the IP, considering active speakers, external traffic policy, active endpoints, node selectors and more.
2. It sorts a hash of "node+VIP" elements. The first item announces.

Consequences:
- Removing a node does not change the speaker announcing the VIP.
- Adding a node changes it only if the new node becomes first in the list.
- Split brain: if a speaker wrongly sees nodes as inactive, it computes a different list, so multiple or no speakers may announce the same VIP. Check speaker logs and ARP replies (see `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-l2-arping`).

Versus Keepalived (VRRP):
- MetalLB uses memberlist for membership, not VRRP messages.
- No VRRP limit of 255 load balancers per network; any number of IPs while free addresses exist.
- No Virtual Router IDs to configure.
- Cannot interoperate with third-party VRRP-aware routers; that is out of scope by design.
- To clients both look the same: the IP seems to move between machines on failover.

## Checked
2026-11-04. Confirmed against the MetalLB "layer 2 mode" page: election algorithm, adding or removing nodes, brain-split behaviour, Keepalived comparison (255 limit, no Virtual Router IDs, no VRRP interoperability). The troubleshooting pointer matches the Troubleshooting page (brain split visible in speaker logs). Removed an added parenthetical about removing the leader.
Method: documentation only; no commands were run.
