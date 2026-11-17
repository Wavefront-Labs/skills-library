---
id: computing-software.systems-network-administration.dns-dhcp.ip-address-hierarchy-and-aggregates
name: ip-address-hierarchy-and-aggregates
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [ipam, ip-address-hierarchy, aggregates, address-plan, netbox, rir]
level: practitioner
status: verified
description: "Model the address hierarchy in IPAM: RIR aggregates, regional and site supernets, prefixes, ranges and IPs, with roles, VRFs and utilisation roll-up."
sources:
  - https://netboxlabs.com/docs/netbox/en/stable/features/ipam/
  - https://www.ripe.net/publications/docs/ripe-738
  - https://www.rfc-editor.org/rfc/rfc1918
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Address hierarchy and aggregates

A clear hierarchy makes allocation predictable, summarisation possible and utilisation reporting
meaningful.

## Layers
| Layer | Example | Purpose |
|-------|---------|---------|
| Aggregate | 10.0.0.0/8 (RFC 1918), 2001:db8::/32 (RIR allocation) | top of the tree, owned by an RIR/RFC |
| Region / supernet | 10.16.0.0/12 EMEA | summarisable per region/WAN domain |
| Site | 10.16.4.0/22 London | one summary route per site |
| Function prefix | 10.16.4.0/24 users, 10.16.5.0/26 mgmt | VLANs/subnets with roles |
| Range / IP | DHCP range .50-.200, gateway .1 | assignments |

## In NetBox
- Aggregates with RIR (`ARIN`, `RIPE`, `RFC 1918`: NetBox treats RFCs 1918 and 6598 as a sort of private RIR). Aggregates
  cannot overlap each other, so you cannot define both 10.0.0.0/8 and 10.16.0.0/16; the latter would be a container
  prefix grouped under the /8 aggregate.
- Prefixes nest automatically by containment; mark container prefixes `status: container`.
- Roles (users, voice, mgmt, p2p), sites/locations, VLAN links, VRFs for overlapping spaces (each VRF keeps its own
  isolated hierarchy; by default duplicates are allowed within a VRF, and the VRF's "enforce unique space" flag
  forbids them).
- Utilisation (NetBox docs): container prefixes report the share consumed by child prefixes; other prefixes report
  child IP addresses and ranges; aggregates report their child prefixes. "Mark utilized" forces 100%.

## Design rules
- Allocate on bit boundaries per site so each site summarises to one prefix; leave room to grow
  (reserve the adjacent block).
- IPv6: a /48 per site and a /64 per VLAN is a common internal plan (RFC 6177 says /48 is no longer recommended as a
  one-size default for end-site assignment, so size to your sites), with nibble-boundary prefixes (/48, /52, /56, /60,
  /64) so each reverse-DNS zone cut lines up: `2001:db8:1:2::1` reverses to `1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa`.
- Encode as little meaning in octets as possible beyond region/site; meaning goes in IPAM fields.
- Record point-to-point (/31, /127) and loopback (/32, /128) pools as separate role prefixes (RFC 6164 covers /127 on
  inter-router links).

The example table nests correctly (checked with Python `ipaddress`): 10.16.4.0/22 spans 10.16.4.0 to 10.16.7.255, inside
10.16.0.0/12 (10.16.0.0 to 10.31.255.255); 10.16.4.0/24 and 10.16.5.0/26 sit in it without overlapping each other.

## Maintenance
Periodic reconciliation (DHCP leases, ARP/ND tables, DNS) against IPAM finds unrecorded use;
utilisation alarms on site prefixes trigger expansions before exhaustion.

## Verify
- [ ] Every prefix in routing tables falls under a recorded aggregate and site container, and utilisation roll-ups match reality within the reconciliation tolerance.
