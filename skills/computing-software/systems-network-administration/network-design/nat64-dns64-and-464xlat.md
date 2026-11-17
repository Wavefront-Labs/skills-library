---
id: computing-software.systems-network-administration.network-design.nat64-dns64-and-464xlat
name: nat64-dns64-and-464xlat
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6, nat64, dns64, 464xlat, clat, ipv6-only, ipv6-transition]
level: practitioner
status: verified
description: "Design IPv6-only networks that still reach IPv4 with NAT64 and DNS64, 464XLAT CLAT on clients, RFC 8925 option 108, and the apps and DNSSEC cases that break."
sources:
  - https://www.rfc-editor.org/rfc/rfc6146
  - https://www.rfc-editor.org/rfc/rfc6147
  - https://www.rfc-editor.org/rfc/rfc6877
  - https://www.rfc-editor.org/rfc/rfc8925
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT64, DNS64 and 464XLAT

IPv6-only access networks remove IPv4 from clients; translation provides IPv4 reachability.

## Pieces
- **NAT64** (RFC 6146): stateful translator; IPv6 packets to `64:ff9b::/96` + embedded IPv4
  become IPv4 from a pool. Runs on firewalls and routers, or in software such as Jool (an open-source SIIT and NAT64 for Linux).
- **DNS64** (RFC 6147): resolver synthesises AAAA records `64:ff9b::<IPv4>` for names that have only A.
  BIND: `dns64 64:FF9B::/96 { clients { any; }; };` (a `dns64` statement; the BIND reference also
  shows `mapped`, `exclude` and `suffix`, and by default skips synthesis when the client set DO and
  the records have RRSIGs unless `break-dnssec yes`); Unbound: `module-config: "dns64 validator iterator"`
  plus the `dns64-prefix` option.
- **464XLAT** (RFC 6877): CLAT on the client translates IPv4 sockets/literals to IPv6, PLAT
  (= NAT64) translates back. Fixes apps using IPv4 literals or IPv4-only sockets. CLAT support is per client OS and version;
  check each platform's documentation.
- **RFC 8925 DHCP option 108** "IPv6-only preferred": dual-stack-capable clients drop IPv4 on
  networks that advertise it, letting one SSID serve both legacy and IPv6-only clients.
- PREF64 in RAs (RFC 8781) tells clients the NAT64 prefix without DNS tricks.

## What breaks
- IPv4 literals in apps/URLs without CLAT (`http://192.0.2.10/`).
- DNSSEC-validating clients reject synthesised AAAA (validation is done by the resolver, so
  stub clients are usually fine).
- Protocols embedding addresses (SIP, FTP active, some VPNs, games) without ALG.
- Local IPv4-only devices (printers) on the same LAN: keep an IPv4 path or translate.

## Design notes
- Well-known prefix `64:ff9b::/96` cannot be used with non-global IPv4 destinations such as RFC 1918 (RFC 6052 section 3.1: MUST NOT; translators MUST drop them). Synthesis check: 192.0.2.33 -> `64:ff9b::c000:221`;
  use a network-specific prefix if you translate to RFC 1918 servers.
- Size the NAT64 pool and logging like CGNAT (port blocks, retention for lawful requests).

## Verify
- [ ] On an IPv6-only client behind DNS64: `dig AAAA ipv4only.arpa` returns a synthesised address (on a plain resolver the A query returns 192.0.0.170 and 192.0.0.171 and AAAA is empty; checked), IPv4-only sites load, and a CLAT-enabled phone reaches an IPv4 literal.
