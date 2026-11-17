---
id: computing-software.systems-network-administration.network-design.detecting-overlapping-subnets
name: detecting-overlapping-subnets
category: computing-software
field: systems-network-administration
product: network-design
tags: [overlapping-subnets, ip-address-planning, mergers, python-ipaddress, ipam, vpn-conflicts]
level: practitioner
status: verified
description: "Find overlapping IPv4/IPv6 subnets across sites, clouds, VPN partners and acquisitions with Python ipaddress and routing-table exports, and decide renumber vs NAT."
sources:
  - https://docs.python.org/3/library/ipaddress.html
  - https://www.rfc-editor.org/rfc/rfc1918
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting overlapping subnets

Overlaps surface at the worst time: connecting a new VPN partner, peering two VPCs, or day one of
an acquisition. Check before connecting.

## Collect prefixes
- Routing tables (the route-listing command of each platform), cloud route tables, firewall objects.
- IPAM/NetBox export, DHCP scopes, VPN partner's encryption domain, VPC/VNet CIDRs.
- Remote-access VPN pools and home networks (192.168.0.0/24, 192.168.1.0/24 are everywhere).

## Python check
```python
import ipaddress, itertools, csv
nets = []
for row in csv.reader(open("prefixes.csv")):        # source,prefix
    nets.append((row[0], ipaddress.ip_network(row[1], strict=False)))
for (sa, a), (sb, b) in itertools.combinations(nets, 2):
    if a.version == b.version and a.overlaps(b):
        print(f"OVERLAP {sa} {a}  <->  {sb} {b}")
```
`strict=False` tolerates host bits set (10.1.1.5/24; with the default `strict=True` Python raises `ValueError: ... has host bits set`). Run on a sample file it printed the 10.0.0.0/8 vs 10.40.0.0/16, 192.168.1.0/24 vs `192.168.1.5/24` and 2001:db8::/32 vs 2001:db8:1::/48 overlaps, and the single-prefix check returned `['10.0.0.0/8', '10.40.0.0/16']`. For thousands of prefixes, sort by network
address and compare neighbours (O(n log n)), or use a prefix trie.

Quick single-prefix check against a list:
```python
cand = ipaddress.ip_network("10.40.0.0/16")
print([str(n) for _, n in nets if n.overlaps(cand)])
```

## Classify what you find
- Identical prefix at two sites: both cannot be reachable from one routing domain.
- One inside the other (10.0.0.0/8 summary vs 10.40.0.0/16 partner): longest prefix wins and the
  summary owner loses reachability to that slice.
- Overlap only with remote-access user home networks: split-tunnel clients cannot reach that
  internal subnet; pick corporate ranges away from 192.168.0/1.x and 10.0.0.0/24.

## Decide
- Renumber the smaller or newer side when practical (DHCP-heavy user networks renumber easily;
  servers with hard-coded IPs do not).
- Twice-NAT at the boundary for partner connections or as a bridge during migration.
- For cloud: allocate VPC CIDRs from a central IPAM pool to stop new overlaps.

## Verify
- [ ] Script output is empty (or every remaining overlap has an accepted mitigation) before the
  new connection goes live.
