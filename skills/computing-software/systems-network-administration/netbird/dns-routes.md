---
id: computing-software.systems-network-administration.netbird.dns-routes
name: dns-routes
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, dns-routes, domain-routing, keep-routes, dns-router-interval]
level: practitioner
status: docs-checked
description: "Route by domain name in NetBird: resolution interval, keep routes, version requirements, wildcard limits and the DNS forwarder port change to 22054."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/index.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/how-routing-peers-work.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
DNS routes use domains instead of IP ranges: the client resolves them and turns the resulting IPs into routes.

Legacy Routes behaviour:
- Requires v0.28.0+. Wildcard domains are not supported in DNS routes.
- Resolution runs every 60 seconds by default. Change it with `netbird up --dns-router-interval 30s`.
- Keep routes is on by default: existing routes are retained when a domain stops resolving, helping long connections survive IP changes.

Forwarder port: from v0.59.0 the local DNS forwarder moved from 5353 to 22054 (applies when all account peers run v0.59.0+). Routing peers' docs state 22054 for client 0.59.0+ and 5353 for older.

Networks equivalents: a domain, including a wildcard such as `*.nb.test`, can be a Network resource. With Routing Peer DNS Resolution (on by default) the client forwards A/AAAA lookups for the domain to the routing peer's resolver; with it off each client must resolve the name itself.

Avoid mixing domain resources and IP-range resources in the same Network: their policies can leak into each other; use a dedicated network with its own routing peers for domain resources.

## Checked

2026-11-04: read the network routes page (DNS routes) and the routing peers page (forwarder port, DNS resolution, mixed-resource warning). Confirmed the 60 second default and `--dns-router-interval`, keep routes default, v0.28.0 gate, no wildcard in DNS routes, the 5353 to 22054 change in v0.59.0 and the mixed-resource warning. Removed the unstated claims that a wildcard resource covers subdomains only (base domain added separately) and that the routing peer can be given a nameserver.

Method: documentation only; no commands were run.
