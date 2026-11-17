---
id: computing-software.systems-network-administration.netbird.network-routes-legacy
name: network-routes-legacy
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, network-routes, routing-groups, distribution-groups, acl-groups]
level: practitioner
status: docs-checked
description: "Understand deprecated NetBird Routes: routing peers, distribution and ACL groups, creating a route, HA selection, and the access-control bypass caveats."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/index.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/advanced-configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Routes are deprecated for everything except exit nodes; use Networks for new work. Routes need v0.9.0+.

Concepts: a route is an identifier plus CIDR ranges; a routing peer forwards between mesh and private network; a routing group gives automatic HA; distribution groups receive the route; optional ACL groups restrict access (none means unrestricted); masquerade is on by default.

Create: Network Routing > Routes > Add Route; enter identifier, description, range (e.g. `172.31.0.0/16`), routing peer or Peer group, distribution groups. Routing peers must be Linux, Windows, macOS or Docker.

HA: several routes with the same identifier and ranges but different peers. Selection: connection status, metric (lower wins), direct over relayed, latency.

Caveats:
- Routes bypass access control unless configured: reaching the routing peer activates the route, so even an ICMP-only policy can open everything.
- Do not reuse a routing peer for both Routes and Networks; permissions can overflow.
- Services on the peer itself need a separate peer-to-peer policy.

Versus Networks: Networks give per-resource policies, always-on masquerade and built-in redundancy; Routes give per-route ACL groups, configurable masquerade, manual setup.

Debug: `netbird routes list`, `ip route show`, `cat /proc/sys/net/ipv4/ip_forward`, tcpdump on the peer, `netbird networks ls` on a client.

## Checked

2026-11-04. Confirmed against the NetBird Routes and Routes advanced configuration pages: deprecation, v0.9.0, concepts, create steps, HA selection order, access control bypass caveat and permission overflow, Networks versus Routes table, debug commands. Nothing removed.
Method: documentation only; no commands were run.
