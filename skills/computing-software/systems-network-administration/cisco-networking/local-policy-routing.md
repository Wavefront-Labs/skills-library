---
id: computing-software.systems-network-administration.cisco-networking.local-policy-routing
name: local-policy-routing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, local-policy-routing, ip-local-policy, router-originated-traffic, pbr, source-interface]
level: practitioner
status: draft
description: "Steer traffic the router itself originates (syslog, IP SLA, SNMP, tunnels) with ip local policy route-map, and when a source-interface or VRF is the better tool."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-pbr.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local policy routing

Interface PBR (`ip policy route-map`) only affects packets arriving on that interface. Packets the
router generates itself (pings, IP SLA probes, syslog, TACACS, tunnel keepalives, BGP) follow the
routing table unless you apply a local policy.

## Configure
```
ip access-list extended SLA-ISP2
 permit icmp host 198.51.100.2 host 8.8.4.4
route-map LOCAL-PBR permit 10
 match ip address SLA-ISP2
 set ip next-hop 198.51.100.1
ip local policy route-map LOCAL-PBR
```
Classic use: dual ISP with IP SLA tracking. The probe for ISP2 must always leave via ISP2, even
when the default route currently points to ISP1, otherwise the SLA measures the wrong path.

## Verify
```
show ip local policy
show route-map LOCAL-PBR          ! policy match counters increase
debug ip policy                   ! lab only, with an ACL
```

## Prefer simpler tools when they fit
- Source address selection: `logging source-interface`, `ip tacacs source-interface`,
  `snmp-server trap-source`, `ip ssh source-interface`. These fix the source IP, not the path.
- Management traffic in a management VRF: `logging host 10.9.9.9 vrf Mgmt-intf`.
- IP SLA has `source-interface`/`source-ip`, and a static host route for the probe target via ISP2
  is often enough: `ip route 8.8.4.4 255.255.255.255 198.51.100.1`.

Local PBR is for cases where the destination is shared (same target via two paths) and only the
source distinguishes them.

## Gotchas
- `set ip next-hop` to an address that is down: traffic falls back to normal routing silently unless
  you use `set ip next-hop verify-availability ... track N`.
- Local policy also catches routing protocol packets if the ACL is broad; keep ACLs narrow (match
  specific source and destination).
- On IOS XE platforms with hardware forwarding, local policy is processed in software; fine for
  control traffic, not for bulk transfers.

## Verify
- [ ] With ISP1 primary, `show ip sla statistics` for the ISP2 probe still succeeds via ISP2
  (confirm with `traceroute 8.8.4.4 source 198.51.100.2`).
