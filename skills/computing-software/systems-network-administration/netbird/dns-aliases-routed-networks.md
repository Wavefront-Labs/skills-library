---
id: computing-software.systems-network-administration.netbird.dns-aliases-routed-networks
name: dns-aliases-routed-networks
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, dns-aliases, domain-resources, custom-zones, routing-peer-dns]
level: advanced
status: docs-checked
description: "Give friendly DNS names to services behind routing peers by combining Custom Zones A records with Network domain resources and an access policy."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/dns-aliases-for-routed-networks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach `postgres.netbird.internal` instead of an IP, with traffic still routed through the routing peer.

Steps:
1. DNS > Zones: add a zone such as `netbird.internal`, distributed to the relevant groups and the routing peer's group. With Routing Peer DNS Resolution on (default) the routing peer answers only from zones it receives. Enable Search Domain for short names (off by default).
2. Add A records per service (e.g. `postgres` to `192.168.0.68`, `wiki` to `192.168.0.78`).
3. Network Routing > Networks: create a network and add a domain resource per service (e.g. `wiki.netbird.internal`) in a group such as `internal-services`.
4. Policy: developer group to resource group, TCP all ports.
5. Add a routing peer that can reach the private subnet.

Verify on a client: `netbird networks ls` shows each domain with "Selected"; then `psql -h postgres.netbird.internal` or `curl http://wiki.netbird.internal`.

Patterns: separate zones per environment (prod and staging) or per site; CNAME aliases to repoint during an outage without client changes. If you already run internal DNS (AD, BIND, Unbound), point NetBird at those instead.

## Checked

2026-11-04: read the DNS aliases for routed networks page in full. Confirmed the zone, record, network resource, policy and routing peer steps, the search-domain default, routing-peer DNS resolution behaviour, the `netbird networks ls` check and the pattern ideas. Nothing removed.

Method: documentation only; no commands were run.
