---
id: computing-software.systems-network-administration.cisco-networking.hsrpv2-for-ipv6
name: hsrpv2-for-ipv6
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, fhrp, hsrpv2, hsrp-ipv6, ipv6, ipv6-gateway, router-advertisement]
level: practitioner
status: draft
description: "Provide a redundant IPv6 default gateway with HSRPv2 on IOS: virtual link-local, autoconfig VIP, RA behaviour, and checking hosts use the virtual MAC."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhp-xe-16-book/ip6-fhrp-hsrp.html
  - https://www.rfc-editor.org/rfc/rfc4861
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HSRPv2 for IPv6

IPv6 hosts learn their default router from Router Advertisements, using the router's
link-local address. HSRP for IPv6 (requires version 2) gives the group a virtual link-local
address and MAC (0005.73A0.0xxx) and only the **active** router sends RAs for it.

## Configure (both routers, different priorities)
```
interface Vlan10
 ipv6 address 2001:db8:10::2/64
 standby version 2
 standby 110 ipv6 autoconfig           ! virtual link-local derived from the virtual MAC
 standby 110 priority 110
 standby 110 preempt delay minimum 120
 standby 110 track 1 decrement 20
```
`autoconfig` is the normal choice; `standby 110 ipv6 FE80::1` sets an explicit virtual
link-local (handy for static host configs). A global VIP can be added with
`standby 110 ipv6 2001:db8:10::1/64` but hosts route via the link-local anyway.

Use different group numbers for IPv4 and IPv6 groups on the same interface (v2 allows 0-4095).

## Gotchas
- Check which source address the RAs come from: hosts must see the virtual link-local as
  their router, not each switch's real link-local. Confirm on a host and with a capture
  (`icmpv6.type == 134`) rather than assuming; release behaviour varies.
- RA lifetime: if the standby also advertised, hosts would keep both routers and fail
  slowly. Check only the virtual address appears as router on hosts.
- Version 1 cannot do IPv6; changing version resets the group (brief outage).

## Verify
```
show standby Vlan10 | include Virtual|State|Active
show ipv6 interface Vlan10            ! joined FF02::66 (HSRPv2) and virtual link-local
```
On a Linux host: `ip -6 route show default` shows `via fe80::205:73ff:fea0:6e` (virtual; group 110 = 0x6e), and
`ip -6 neigh` maps it to 00:05:73:a0:00:6e.
On Windows: `netsh interface ipv6 show route` / `Get-NetRoute -AddressFamily IPv6 ::/0`.
- [ ] Hosts' default route is the virtual link-local; failover test keeps IPv6 pings flowing.
