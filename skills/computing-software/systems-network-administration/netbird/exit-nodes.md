---
id: computing-software.systems-network-administration.netbird.exit-nodes
name: exit-nodes
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, exit-nodes, default-route, block-lan-access, dns-leak]
level: practitioner
status: docs-checked
description: "Configure a NetBird exit node: the 0.0.0.0/0 route, what it exposes, IPv6 behaviour, required ICMP policy, Block LAN access and preventing DNS leaks."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/index.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/how-routing-peers-work.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An exit node is a default route (`0.0.0.0/0`) that sends all internet traffic from peers in its distribution groups through a routing peer. It is the one use case that still belongs under Routes.

Points to know:
- It grants access to everything the routing peer can reach, including its LAN. Use the Block LAN access option to limit this.
- IPv6 is blocked.
- Clients need an ICMP policy to reach the exit node.
- Set a DNS server with match domain `ALL` to prevent DNS leaks.
- Create it under Network Routing > Routes with the range `0.0.0.0/0`, a routing peer or group, and distribution groups.
- Multiple exit nodes follow normal HA selection: connection status, lower metric, direct over relayed, latency.

Because routes bypass access control unless configured, scope distribution groups tightly.

## Checked

2026-11-04. Confirmed against the NetBird Routes and How Routing Peers Work pages: 0.0.0.0/0 default route, deprecated Routes except exit nodes, LAN exposure and Block LAN access, IPv6 blocked, minimum ICMP policy, DNS match domain `ALL`, HA selection order, Routes bypassing access control by default. Removed the client-side `--block-lan-access` and `networks select` line, which neither page documents.
Method: documentation only; no commands were run.
