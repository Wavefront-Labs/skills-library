---
id: computing-software.systems-network-administration.cisco-networking.dhcpv6-pd-client-general-prefix
name: dhcpv6-pd-client-general-prefix
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, general-prefix, dhcpv6-pd-client, prefix-delegation, ipv6, branch-router, isp]
level: practitioner
status: draft
description: "Get an IPv6 prefix from an ISP via DHCPv6-PD on an IOS XE router and number LANs from it with a general prefix, so a changing delegated prefix renumbers automatically."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6_basic/configuration/xe-16/ip6b-xe-16-book/ip6-dhcp-prefix-xe.html
  - https://www.rfc-editor.org/rfc/rfc8415#section-6.3
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCPv6-PD client and general prefix on IOS XE

ISPs delegate a prefix (often /56 or /48) to the customer router. A general prefix is a named
placeholder for whatever prefix arrives; LAN interfaces are numbered relative to it.

## Request the prefix on the WAN
```
ipv6 unicast-routing
interface GigabitEthernet0/0/0
 description ISP
 ipv6 address autoconfig default        ! WAN address via SLAAC + default route from RA
 ipv6 dhcp client pd ISP-PD rapid-commit
 ipv6 nd autoconfig default-route
```
Some ISPs give the WAN address via DHCPv6 IA_NA: `ipv6 address dhcp`.

## Number LANs from it
```
interface Vlan10
 ipv6 address ISP-PD ::10:0:0:0:1/64    ! subnet 10 of the delegated prefix, host ::1
interface Vlan20
 ipv6 address ISP-PD ::20:0:0:0:1/64
```
If the ISP delegates 2001:db8:abcd:ff00::/56, Vlan10 becomes 2001:db8:abcd:ff10::1/64. The subnet
ID must fit inside the delegated bits (/56 gives 00-ff in the fourth hextet's low byte).

## Hand addresses to hosts
RA with SLAAC is automatic on the LAN interfaces. For DNS, stateless DHCPv6:
```
ipv6 dhcp pool LAN-STATELESS
 import dns-server
 import domain-name
interface Vlan10
 ipv6 nd other-config-flag
 ipv6 dhcp server LAN-STATELESS
```
`import` reuses what the ISP gave you in the PD exchange.

## Verify
```
show ipv6 dhcp interface GigabitEthernet0/0/0
!  Prefix name: ISP-PD  Prefix: 2001:DB8:ABCD:FF00::/56 preferred lifetime ...
show ipv6 general-prefix
show ipv6 interface brief
```

## Gotchas
- Delegated prefixes can change on reconnect with residential/SMB ISPs. Anything hard-coding the
  prefix (firewall rules, DNS AAAA records) breaks; reference the general prefix or use ULA for
  internal services.
- Inbound ACL on the WAN must permit DHCPv6 replies (UDP 547 -> 546) and ICMPv6 ND, or PD fails
  silently.
- Add an inbound IPv6 filter/zone firewall: once PD works, LAN hosts are globally reachable.
- Prefix lost on reboot until the ISP renews; some ISPs require the same DUID to give the same
  prefix (keep the router's DUID stable).

## Verify
- [ ] LAN hosts get global addresses from the delegated prefix and reach `ipv6.google.com`.
