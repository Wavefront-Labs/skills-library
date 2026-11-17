---
id: computing-software.systems-network-administration.cisco-networking.multicast-boundaries-and-scoping
name: multicast-boundaries-and-scoping
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, multicast, multicast-boundary, ip-multicast-boundary, ttl-threshold, admin-scoping, auto-rp-filter]
level: practitioner
status: docs-checked
description: "Plan multicast scope boundaries with RFC 2365 administratively scoped addresses (239.255.0.0/16, 239.192.0.0/14) and why they beat TTL thresholds."
sources:
  - https://datatracker.ietf.org/doc/html/rfc2365
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicast boundaries and scoping

## Scoping model (RFC 2365)
The administratively scoped IPv4 multicast space is 239.0.0.0 to 239.255.255.255.

| Scope | Range | Notes |
|---|---|---|
| Link-local | 224.0.0.0/24 | statically assigned |
| IPv4 Local Scope | 239.255.0.0/16 | minimal enclosing scope; a Local Scope must be contained within or equal to any larger scope |
| IPv4 Organization Local Scope | 239.192.0.0/14 | for use in defining private scopes |
| Global | 224.0.1.0-238.255.255.255 | static global allocations |

- Packets to administratively scoped addresses do not cross configured boundaries, and the addresses are locally
  assigned (not globally unique).
- A router should support per-interface configuration of a scope boundary for the scoped range. Any scope boundary
  is also a boundary for the Local Scope: 239.255.0.0/16 traffic must not be forwarded across a link with a scope
  boundary defined.
- A scope region must be connected (a path between any two nodes that stays inside it). If scope regions intersect,
  the outer scope is its address space minus the intersecting scopes.
- The high-order /24 of each scope is reserved for relative-address use (in the Local Scope,
  239.255.255.0/24).
- 239.0.0.0/10, 239.64.0.0/10 and 239.128.0.0/10 are unassigned and should stay unassigned until
  239.192.0.0/14 is no longer sufficient.

## TTL thresholds versus address scoping
RFC 2365 describes the TTL threshold rule: a packet is forwarded only if its remaining TTL is greater than the
interface threshold. It says TTL scoping has proven difficult to implement reliably because the TTL also limits
datagram lifetime, and that with broadcast-and-prune protocols it can prevent pruning from being effective;
administratively scoped addresses give clear and simple semantics. Prefer address boundaries over TTL thresholds.

## Cisco configuration
The Cisco boundary page was unreadable when this skill was checked, so command syntax is not given here. Use the
`ip multicast boundary` command (with an access list of the groups to block) from the command reference for your
release, and check behaviour with its documented `show` commands.

## Checked
Checked 2026-11-08 against RFC 2365 (sections on administratively scoped space, scopes, and TTL scoping). Removed:
Cisco configuration examples, `filter-autorp` and `in`/`out` keyword behaviour, SSDP and mDNS remarks, and `show`
commands, because the Cisco documentation page returned 404.
Method: documentation only; no commands were run.
