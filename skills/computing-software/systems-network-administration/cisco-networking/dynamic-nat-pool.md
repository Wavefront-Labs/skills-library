---
id: computing-software.systems-network-administration.cisco-networking.dynamic-nat-pool
name: dynamic-nat-pool
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, nat, dynamic-nat, nat-pool, ip-nat-pool, prefix-length, nat-acl]
level: practitioner
status: docs-checked
description: "Translate inside hosts to a pool of public addresses with dynamic NAT on IOS: pool, ACL, overload, translation timeouts and the permit-any restriction."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-addr-consv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic NAT with a pool

Dynamic NAT translates each inside host to an address allocated as needed from a pool of global addresses.
Adding `overload` instead translates many inside hosts to the same pool address (PAT).

```
ip nat pool net-208 172.16.233.208 172.16.233.223 prefix-length 28
access-list 1 permit 192.168.201.0 0.0.0.255
ip nat inside source list 1 pool net-208
interface Gi0/0/0
 ip nat outside
interface Gi0/0/1
 ip nat inside
```
- `ip nat pool name start-ip end-ip {netmask netmask | prefix-length prefix-length}` defines the pool; use either
  keyword (the Cisco examples show both).
- The access list must permit ONLY the addresses to be translated; it has an implicit deny all at the end, and an
  access list that is too permissive can give unpredictable results. NAT does not support `permit ip any any` in
  an access list used with a NAT command.
- `ip nat inside source list {access-list-number | access-list-name} pool pool-name [overload]`.
- When inside global addresses belong to a directly connected subnet, the device adds IP aliases for them so it
  answers ARP requests. Cisco warns this can make the device answer packets not destined for it (for example an
  ICMP or UDP packet to an aliased address with no translation, when the device runs a matching service such as NTP).

## Overload instead of one-to-one
```
ip nat inside source list 1 pool net-208 overload
```
Overload (PAT) supports only protocols whose port numbers are known: ICMP, TCP and UDP. Other protocols consume
the entire address, so they do not work with PAT.

## Translation timeouts
- When overload is not configured, simple (dynamic) translation entries time out after 24 hours by default. The
  timeout is changed with the `ip nat translation timeout` command (the Cisco task shows the form
  `ip nat translation seconds`, for example `ip nat translation 300`).
- `ip nat translation udp-timeout seconds` changes the UDP timeout (default 300 seconds); it applies only when the
  general translation timeout is not configured.
- `ip nat translation max-entries` changes the global translation limit.

## Verify
```
show ip nat statistics
show ip nat translations
```
`show ip nat statistics` displays all configured pools and NAT mappings; with many pools and mappings its
statistics update slowly.
- [ ] Inside hosts show translations from the pool; hosts outside the permit list are untranslated.

## Checked
Date: 2026-11-07. The IOS XE NAT address-conservation chapter (about 88k characters) was searched and read around the
pool, access list, `ip nat inside source`, overload, ARP alias note, PAT restrictions, timeout and statistics
sections; it was not read cover to cover. The 13772-12 how-to (about 19k) was read for its pool and overload
configuration.
Confirmed: pool syntax with both netmask and prefix-length, ACL guidance and the `permit ip any any` restriction,
`ip nat inside source` forms, 24-hour default, UDP timeout default, `max-entries`, PAT protocol restriction, show commands.
Removed (not on the pages): the `misses` and `allocated 16 (100%)` pool-exhaustion output and the 16-host
arithmetic, "a deny means do not NAT", the route-map plus `ip nat inside source route-map ... pool` VPN-exclusion
recipe (the page documents route-map only on static mappings), the "86400 s" figure (the page says 24 hours) and the
claim that `prefix-length` must cover the pool range.
Method: documentation only; no commands were run.
