---
id: computing-software.systems-network-administration.cisco-networking.nat-hairpin-and-nvi
name: nat-hairpin-and-nvi
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, nat, nat-hairpin, nat-nvi, nat-loopback, ip-nat-enable, split-dns]
level: practitioner
status: draft
description: "Let inside clients reach an inside server by its public address on IOS using NAT Virtual Interface (ip nat enable), or avoid hairpinning with split DNS."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/112084-nat-hairpin-00.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-nvi.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT hairpinning and NVI

Problem: an inside client resolves `www.example.com` to the public 203.0.113.10, which is
statically NATed to 10.1.1.10 inside. Classic inside/outside NAT never translates traffic
that enters and leaves inside interfaces, so the connection fails.

## Preferred fix: split DNS
Serve the inside address to inside clients (internal zone or DNS view). No hairpin, no extra
router load, server sees real client IPs. Use this whenever you control DNS.

## NVI fix (domain-less NAT)
Replace `ip nat inside/outside` with `ip nat enable` on all involved interfaces and drop the
`inside`/`outside` keywords from rules:
```
interface Gi0/0/0
 ip nat enable
interface Gi0/0/1
 ip nat enable
ip nat source static 10.1.1.10 203.0.113.10
ip nat source list NAT-INSIDE interface Gi0/0/0 overload
```
NVI translates any packet whose destination matches a mapping, regardless of direction, so
LAN->public->LAN works. The server sees the client translated to the overload address unless
you add an exclusion; client IP logging is lost.

## Gotchas
- Not every platform supports NVI: Cisco's IOS-XE NAT guides list NVI (`ip nat enable`)
  as unsupported; on those, use split DNS or a policy hairpin design.
- Mixing NVI and classic inside/outside on the same router is unsupported.
- `show ip nat nvi translations` and `show ip nat nvi statistics` replace the normal show commands.

## Verify
```
show ip nat nvi translations
```
From an inside host: `curl -v http://203.0.113.10/` succeeds.
- [ ] Inside access by public name works (split DNS or NVI) and external access unchanged.
