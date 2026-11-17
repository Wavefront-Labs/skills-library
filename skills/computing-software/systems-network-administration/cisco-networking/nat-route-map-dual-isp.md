---
id: computing-software.systems-network-administration.cisco-networking.nat-route-map-dual-isp
name: nat-route-map-dual-isp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, nat-route-map, dual-isp, pat, ip-sla, failover, match-interface]
level: practitioner
status: docs-checked
description: "PAT to two ISPs on one IOS router with route-map based NAT: translate to the egress interface's address, with tracked default routes for failover."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13739-nat-routemap.html
  - https://www.cisco.com/c/en/us/support/docs/ip/ip-routing/200785-ISP-Failover-with-default-routes-using-I.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT with route-maps for dual ISP

Cisco's NAT route-map technote states that route-maps with NAT suit a subscriber multi-homed to different ISPs,
because under `match` a route-map can use the egress interface or next hop as well as the source address.

## How route-map NAT behaves
- NAT consults an access list or route-map only when it needs to create a translation entry; an existing entry that
  matches the traffic is used without consulting either.
- A route-map always creates a fully extended entry (inside and outside local/global plus TCP or UDP port). An
  access-list rule without overload creates a simple entry with addresses only, which can wrongly catch traffic to
  other destinations (the technote's two-destination example) and can be used by any outside host.
- So translations created before a failover keep their original inside global address; new flows are translated by the
  rule that matches the new egress interface.

## Configuration (follows the technote's NAT failover example)
```
interface GigabitEthernet0/0/1
 description PRIMARY LINK TO ISP 1
 ip nat outside
interface GigabitEthernet0/0/0
 description BACKUP LINK TO ISP 2
 ip nat outside
interface GigabitEthernet0/0/2
 description TOWARDS CUSTOMER LAN
 ip nat inside

ip access-list extended 101
 permit ip 192.168.1.0 0.0.0.255 any

route-map NAT_ISP1 permit 10
 match ip address 101
 match interface GigabitEthernet0/0/1
route-map NAT_ISP2 permit 10
 match ip address 101
 match interface GigabitEthernet0/0/0

ip nat inside source route-map NAT_ISP1 interface GigabitEthernet0/0/1 overload
ip nat inside source route-map NAT_ISP2 interface GigabitEthernet0/0/0 overload
```
This enables PAT: the route-map selects what is translated and the address after `interface` is what it is translated
into.

## Routing with failover
```
ip sla 1
 icmp-echo <PROBE_TARGET> source-ip <ISP1_INTERFACE_ADDRESS>
ip sla schedule 1 life forever start-time now
track 8 ip sla 1 reachability

ip route 0.0.0.0 0.0.0.0 <ISP1_NEXT_HOP> track 8
ip route 0.0.0.0 0.0.0.0 <ISP2_NEXT_HOP> 10
```
While track 8 is up the default goes via ISP 1; when it is down the default (administrative distance 10) goes via
ISP 2. In the technote, NAT translations then appeared using the ISP 2 interface address, and moved back when the
primary returned. Cisco recommends IP SLA threshold 5000 ms, timeout 5000 ms and frequency 60 s.

## Verify
```
show ip nat translations
show track
show ip route static
```
- [ ] With ISP 1 up, inside globals use the ISP 1 interface address.
- [ ] With the tracked route down, new flows use the ISP 2 interface address.

## Checked
Checked 2026-11-08 against Cisco's NAT route-map technote (document 13739, which dates from IOS 12.3) and the ISP
Failover with default routes using IP SLA technote (document 200785, revised November 2023): route-map NAT behaviour,
the dual-ISP route-map and `interface ... overload` syntax, the tracked default and floating route, the
recommended IP SLA values and verify commands. Removed as unconfirmed by readable pages: `source-interface` probes,
track delays, the probe host route, the EEM applet, `clear ip nat translation *`, the 24 hour TCP timeout, and the
uRPF, static NAT and IPsec gotchas. The IOS XE NAT configuration book page was a stub, so nothing relies on it.
Method: documentation only; no commands were run.
