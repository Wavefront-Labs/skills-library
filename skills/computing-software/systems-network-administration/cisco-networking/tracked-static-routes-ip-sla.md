---
id: computing-software.systems-network-administration.cisco-networking.tracked-static-routes-ip-sla
name: tracked-static-routes-ip-sla
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, static-route, static-routing, tracked-static-route, ip-sla-tracking, ip-sla, icmp-echo, track, dual-isp, failover, floating-static-route, reachability]
level: practitioner
status: docs-checked
description: "Fail over a default route between ISPs with IP SLA probes, a track object, a tracked primary static route and a floating backup, plus NAT per ISP and testing."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/ip-routing/200785-ISP-Failover-with-default-routes-using-I.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracked static routes with IP SLA

Cisco's technote covers WAN or ISP redundancy where multiple links end on the same router, using static routing, an
IP SLA and a track object.

## Configure (from the technote)
```
track 8 ip sla 1 reachability

ip sla 1
 icmp-echo <PROBE_TARGET> source-ip <ISP1_INTERFACE_ADDRESS>
ip sla schedule 1 life forever start-time now

ip route 0.0.0.0 0.0.0.0 <ISP1_NEXT_HOP> track 8     ! primary, present only while track 8 is up
ip route 0.0.0.0 0.0.0.0 <ISP2_NEXT_HOP> 10           ! backup, administrative distance 10
```
- Track 8 up: `show ip route static` shows `S* 0.0.0.0/0 [1/0]` via the ISP 1 next hop.
- Track 8 down: it shows `S* 0.0.0.0/0 [10/0]` via the ISP 2 next hop.
- When the primary comes back, traffic returns to it automatically.
- Cisco recommends these IP SLA values: threshold 5000 ms, timeout 5000 ms, frequency 60 s.
- The technote's probe targets the ISP 1 next hop address; choose a target whose loss means the primary path is
  unusable.

## NAT with dual ISPs
The technote adds route-maps matching an ACL and the egress interface, so sessions translate to the right ISP's
address:
```
route-map NAT_ISP1 permit 10
 match ip address 101
 match interface GigabitEthernet0/0/1
ip nat inside source route-map NAT_ISP1 interface GigabitEthernet0/0/1 overload
```
See nat-route-map-dual-isp for the full pair of rules. In the test, `show ip nat translations` showed the ISP 1
interface address while the primary was up and the ISP 2 address after it failed.

## Verify
```
show track
show ip route static
show ip nat translations
```
`show track` reports `IP SLA 1 reachability`, `Reachability is Up` and the change count, and `Tracked by: Static IP
Routing`. The technote says troubleshooting should centre on the static route, IP SLA and track configuration, and on
why the primary link failed.
- [ ] Failing the primary probe switches the default to the backup route; restoring it switches back.

## Checked
Checked 2026-11-08 against Cisco's ISP Failover with default routes using IP SLA technote (document 200785,
revised November 2023): syntax, the AD 10 backup, recommended IP SLA values, NAT route-maps and verify output.
Removed as unconfirmed: `source-interface`, `threshold`/`timeout`/`frequency` example values, track `delay`, the probe
host route, track lists, target choice advice, `clear ip nat translation *`, and the `%TRACK-6-STATE` message. The IP
SLA configuration book page was a stub.
Method: documentation only; no commands were run.
