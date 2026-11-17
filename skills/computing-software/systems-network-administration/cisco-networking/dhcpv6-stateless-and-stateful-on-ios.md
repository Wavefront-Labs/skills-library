---
id: computing-software.systems-network-administration.cisco-networking.dhcpv6-stateless-and-stateful-on-ios
name: dhcpv6-stateless-and-stateful-on-ios
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ipv6, ipv6-configuration, dhcpv6, stateless-dhcpv6, stateful-dhcpv6, ipv6-dhcp-pool, managed-config-flag, other-config-flag, ipv6-dhcp-relay, slaac, router-advertisement, rdnss]
level: practitioner
status: draft
description: "Hand out IPv6 settings from IOS: SLAAC only, SLAAC plus stateless DHCPv6 (O flag), stateful DHCPv6 (M flag), DHCPv6 relay, RA flags and why Android ignores DHCPv6."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book/ip6-dhcp-stateless.html
  - https://datatracker.ietf.org/doc/html/rfc8415
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateless and stateful DHCPv6 on IOS

Hosts get IPv6 addresses from Router Advertisements (SLAAC) and/or DHCPv6. The **RA flags**
decide which: `M` (managed) = get addresses from DHCPv6; `O` (other) = get DNS/domain from
DHCPv6. Default gateway always comes from RAs, never DHCPv6.

## SLAAC + stateless DHCPv6 (common)
```
ipv6 dhcp pool V6-STATELESS
 dns-server 2001:db8:53::53
 domain-name corp.example
interface Vlan10
 ipv6 address 2001:db8:10:10::1/64
 ipv6 nd other-config-flag                 ! O=1
 ipv6 dhcp server V6-STATELESS
 ipv6 nd ra dns server 2001:db8:53::53     ! RDNSS in RA too (IOS XE 16.x+), for Android
```

## Stateful DHCPv6
```
ipv6 dhcp pool V6-STATEFUL
 address prefix 2001:db8:10:20::/64 lifetime 172800 86400
 dns-server 2001:db8:53::53
interface Vlan20
 ipv6 address 2001:db8:10:20::1/64
 ipv6 nd managed-config-flag               ! M=1
 ipv6 nd prefix default no-autoconfig      ! A=0: stop SLAAC addresses as well
 ipv6 dhcp server V6-STATEFUL
```

## Relay to a central server (Kea, Windows)
```
interface Vlan20
 ipv6 dhcp relay destination 2001:db8:53::547
```
The relay inserts the interface-id; the server needs a subnet matching the link address.

## Client behaviour gotchas
- **Android does not implement DHCPv6** address assignment: it needs SLAAC (A=1) and gets DNS
  from RDNSS in RAs. An M=1, A=0 network leaves Android with link-local only.
- Windows and macOS support both; Windows also sends a DHCPv6 solicit when M=1.
- DHCPv6 identifies clients by **DUID**, not MAC: reservations by MAC are unreliable.

## Verify
```
show ipv6 dhcp pool
show ipv6 dhcp binding
show ipv6 interface Vlan20 | i flag|hosts use
debug ipv6 dhcp detail       ! lab
```
Client: `ipconfig /all` (DHCPv6 IAID/DUID, DNS), Linux `ip -6 addr` (dynamic, mngtmpaddr).
- [ ] RA flags match design (`show ipv6 interface` "Hosts use DHCP to obtain ...").
- [ ] A Windows, macOS and Android client each get a global address and DNS.
