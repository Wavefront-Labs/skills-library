---
id: computing-software.systems-network-administration.cisco-networking.policy-based-routing-route-map
name: policy-based-routing-route-map
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, path-control, policy-based-routing, pbr, set-ip-next-hop, ip-policy-route-map, route-map, verify-availability, local-policy, set-ip-default-next-hop, source-routing, pbr-verify-availability]
level: practitioner
status: draft
description: "Steer traffic by source or application with PBR on IOS: route-map match/set, next-hop vs default next-hop, tracked next hops, local policy for router-originated traffic, verifying."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-pbr.html
  - https://www.cisco.com/c/en/us/support/docs/ip/ip-routing/47121-pbr-cmds-ce.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy-based routing

PBR overrides the routing table for packets **entering** an interface, based on an ACL match
(source, protocol, ports), not just destination.

## Example: guest VLAN out the cheap ISP
```
ip access-list extended GUEST-NETS
 permit ip 10.90.0.0 0.0.255.255 any
!
ip sla 20
 icmp-echo 198.51.100.1
ip sla schedule 20 life forever start-time now
track 20 ip sla 20 reachability
!
route-map PBR-GUEST permit 10
 match ip address GUEST-NETS
 set ip next-hop verify-availability 198.51.100.1 1 track 20
!
interface Vlan90
 ip policy route-map PBR-GUEST
```
Packets not matching any permit clause (or matching a deny clause) are routed normally.

## set options
| Command | Behaviour |
|---|---|
| `set ip next-hop X` | use X even if the RIB has a better route; if X unreachable (not connected / not in ARP) fall back to RIB |
| `set ip next-hop verify-availability X seq track N` | use X only while track N is up |
| `set ip default next-hop X` | use X only if the RIB has **no explicit route** (default route ignored) |
| `set interface Tunnel1` | point-to-point exit |
| `set ip next-hop recursive X` | X need not be directly connected |
| `set vrf NAME` | VRF selection |

## Router-originated traffic
`ip local policy route-map NAME` applies PBR to packets the router itself generates (e.g. IP SLA
probes, syslog), which interface `ip policy` does not touch.

## Verify
```
show route-map PBR-GUEST          ! "Policy routing matches: N packets"
show ip policy                    ! interfaces with policies
debug ip policy                   ! lab only; process-level detail
traceroute 8.8.8.8 source Vlan90  ! from the router uses local policy only, test from a host
```

## Gotchas
- PBR is ingress only: apply on the interface where the traffic arrives (the LAN SVI), not the
  WAN.
- Return traffic follows normal routing: with NAT on each ISP it returns correctly; without,
  asymmetric paths break stateful firewalls.
- Hardware support: on Catalyst switches PBR is in TCAM; ACLs with `deny` lines or unsupported
  sets may punt to the CPU. Check platform guides.
- Keep a clause for the local subnets (`deny` to internal ranges) so internal traffic is not
  pushed to the ISP.

## Verify
- [ ] Match counters increase for guest traffic only.
- [ ] Traceroute from a guest host exits ISP2; from a staff host exits ISP1.
- [ ] Failing track 20 sends guest traffic via the normal default.
