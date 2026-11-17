---
id: computing-software.systems-network-administration.network-design.network-renumbering
name: network-renumbering
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-renumbering, ip-migration, dhcp, dns-ttl, address-planning]
level: practitioner
status: docs-checked
description: "Renumber a site or subnet with minimal outage: inventory hard-coded IPs, lower DNS TTLs, overlap old and new ranges, migrate DHCP and statics in waves, then clean up."
sources:
  - https://www.rfc-editor.org/rfc/rfc2071
  - https://www.rfc-editor.org/rfc/rfc4192
  - https://www.rfc-editor.org/rfc/rfc6879
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network renumbering

Reasons: overlapping RFC 1918 space after a merger, IPAM clean-up, moving to a cloud-compatible
plan, ISP or PI changes.

## 1. Inventory what references addresses
- DHCP scopes, reservations, options (DNS, NTP, boot/TFTP).
- Statically addressed devices: servers, printers, cameras, OT, UPS, BMCs. Find them by ARP vs DHCP
  lease diff: hosts in ARP tables without a lease are static.
- Firewall objects, ACLs, NAT, VPN encryption domains (partners!), routing filters, SNMP/syslog
  allow-lists, licence servers bound to IP, application configs, hosts files, scripts.
- Search configs and repos: `grep -rE '10\.20\.[0-9]+\.[0-9]+'`.

## 2. Prepare
- Lower DNS TTLs at least one old-TTL period before (RFC 4192 also advises reducing DNS TTLs and having DHCP clients contact the server more often).
- Get new firewall/partner VPN changes approved early; partners are the long pole.
- Add the new subnet alongside the old (secondary address or new VLAN), route and permit both.

## 3. Migrate in waves
1. DHCP: add the new scope, shorten the old lease time well ahead, then deactivate the old
   scope; clients move on renewal.
2. Static hosts by group with owners present; update DNS A and PTR in the same change.
3. Infrastructure last (gateways, management), keeping out-of-band access.

IPv6 has protocol support for this (RFC 4192): advertise the new prefix, deprecate the old with
preferred lifetime 0, then remove.

## 4. Clean up
Remove old scopes, secondaries, objects and rules; restore DNS TTLs; update IPAM, diagrams,
monitoring targets.

## Verify
- [ ] No traffic sourced from the old range for a full business cycle (flow data / firewall logs), then old range withdrawn.

## Checked

2026-10-28: Confirmed in RFC 4192: renumbering may need reduced DNS TTLs and more frequent DHCP client contact, and old-prefix preferred lifetimes are set to zero before removal. Removed the 300 s TTL, the 1 h lease and the DHCP option numbers 150/66, which the fetched RFCs (2071, 4192, 6879) do not state.
Method: documentation only; no commands were run.
