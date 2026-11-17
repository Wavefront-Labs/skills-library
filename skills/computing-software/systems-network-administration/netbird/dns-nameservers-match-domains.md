---
id: computing-software.systems-network-administration.netbird.dns-nameservers-match-domains
name: dns-nameservers-match-domains
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, dns, nameservers, match-domains, search-domains, platform-dns]
level: practitioner
status: docs-checked
description: "Configure NetBird nameservers: primary versus match-domain routing, search domains, per-platform DNS behaviour, Android Private DNS and the routing peer forwarder port."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add nameservers in the dashboard under DNS > Nameservers.

Routing:
- A nameserver with no match domains is the primary and handles all queries no other rule matches.
- A match domain such as `company.internal` sends queries for it (and subdomains) to a specific nameserver; the most specific match wins.
- Search domains (v0.24.0+) let short names like `server1` resolve under `company.internal`.
- NetBird does not cache most queries (exceptions: routing-peer forwarder during upstream failure, NetBird's own infrastructure addresses).

Platform behaviour:
- Linux: DNS is always configured, so peer names work without custom nameservers; original nameservers stay as upstreams.
- macOS, Windows, mobile: DNS changes only when nameservers are configured; otherwise use NetBird IPs.
- Android: turn Private DNS off, or Android bypasses VPN DNS.
- Match domains are supported only on macOS, Windows 10+, and Linux with `systemd-resolved`. Assign a primary nameserver to all peers as a baseline.

Network resources: routing peers run a DNS forwarder for domain-based resources on port `22054`, or `5353` if any peer is below v0.59.0. Test: `nslookup -port=22054 <domain> <routing-peer-ip>`.

Related: for internal DNS servers (AD, BIND) the docs moved the nameserver guide to the Internal DNS Servers page.

## Checked

2026-11-04: read the DNS overview page in full. Confirmed primary and match-domain routing, most-specific-match rule, the v0.24.0 search-domain gate, the no-cache note and its exceptions, per-platform behaviour, the Android Private DNS note, match-domain platform support and the forwarder port change (22054, with 5353 kept while any peer is below v0.59.0). Nothing removed.

Method: documentation only; no commands were run.
