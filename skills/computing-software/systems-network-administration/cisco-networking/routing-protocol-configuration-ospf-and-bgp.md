---
id: computing-software.systems-network-administration.cisco-networking.routing-protocol-configuration-ospf-and-bgp
name: routing-protocol-configuration-ospf-and-bgp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, routing, dynamic-routing, ospf, ospfv2, ospf-area, area-0, abr, stub-area, passive-interface, router-id, reference-bandwidth, ospf-neighbor, exstart, mtu-mismatch, ospf-authentication, bgp, ebgp, ibgp, autonomous-system, asn, prefix-list, route-map, maximum-prefix, next-hop-self, update-source, local-preference, as-path-prepend, med, bgp-best-path, soft-reconfiguration, multihoming, ospf-adjacency, ospf-neighbor-states, ip-ospf-area]
level: advanced
status: draft
description: "Configure OSPF (areas, passive-by-default, p2p links, auth, reference bandwidth, stuck-neighbour causes) and BGP (eBGP/iBGP, prefix-list filters, max-prefix, local-pref/prepend) on IOS."
sources:
  - https://datatracker.ietf.org/doc/html/rfc2328
  - https://datatracker.ietf.org/doc/html/rfc4271
  - https://datatracker.ietf.org/doc/html/rfc8212
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Routing protocol configuration: OSPF and BGP — explicit adjacencies, filtered everything

**Goal:** bring up OSPF inside a site/campus and BGP at the edge (ISP or between sites)
so adjacencies form only where intended, routes are filtered, and you can prove the path.
Examples use documentation prefixes and private ASNs (64512–65534).

## 1. OSPF baseline
```
router ospf 1
 router-id 10.255.0.1                  ! fixed; never let it pick an interface IP
 auto-cost reference-bandwidth 100000  ! 100 Gb/s; same value on EVERY router
 passive-interface default
 no passive-interface TenGigabitEthernet1/1/1
!
interface TenGigabitEthernet1/1/1
 ip ospf 1 area 0
 ip ospf network point-to-point        ! no DR/BDR election on a 2-router link
interface Loopback0
 ip ospf 1 area 0
interface Vlan10
 ip ospf 1 area 0                      ! advertised, but passive: no hellos to users
```
- The default reference bandwidth (100 Mb/s) makes 1G, 10G and 100G all cost 1, so OSPF
  cannot tell them apart.
- `passive-interface default` stops rogue adjacencies from user VLANs; un-passive only
  router-facing links.
- Interface-level `ip ospf 1 area 0` is clearer than `network` wildcard statements.
- **Authentication:** IOS-XE supports HMAC-SHA via key chains
  (`ip ospf authentication key-chain OSPF-KC` with `cryptographic-algorithm hmac-sha-256`);
  older images only MD5 (`ip ospf message-digest-key 1 md5 <KEY>`). Confirm on your image.

## 2. OSPF areas
- Area 0 is the backbone; every other area must touch it via an ABR.
- Summarise at the ABR: `area 1 range 10.1.0.0 255.255.0.0`. This only works if the area's
  addressing is contiguous (see `...network-design.subnetting-and-ip-address-planning`).
- `area 1 stub` (no external LSAs) or `area 1 stub no-summary` (totally stubby, ABR only)
  for branch areas with one exit. All routers in the area must agree.
- One flat area 0 is fine for a few dozen routers; split when SPF churn or LSDB size
  becomes a problem, not by habit.

## 3. Why OSPF neighbours don't form
| `show ip ospf neighbor` state | Cause |
|---|---|
| Nothing at all | interface passive, ACL blocking 224.0.0.5/6 (protocol 89), different subnet/mask, area ID mismatch |
| INIT | hellos one-way only (ACL, unidirectional link) |
| 2WAY | normal between two DROTHERs on a broadcast segment |
| EXSTART/EXCHANGE stuck | **MTU mismatch** (fix the MTU; `ip ospf mtu-ignore` is a workaround) |
| Flapping | hello/dead timers differ, auth key mismatch, duplicate router-id |
`debug ip ospf adj` (briefly, with logging buffered) names the mismatch.

## 4. BGP edge with an ISP
```
router bgp 64512
 bgp router-id 10.255.0.1
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 203.0.113.1 remote-as 64500
 neighbor 203.0.113.1 description ISP-A
 neighbor 203.0.113.1 password <BGP_MD5_KEY>
 address-family ipv4 unicast
  network 198.51.100.0 mask 255.255.255.0
  neighbor 203.0.113.1 activate
  neighbor 203.0.113.1 prefix-list OUR-PREFIXES out
  neighbor 203.0.113.1 prefix-list FROM-ISP-A in
  neighbor 203.0.113.1 maximum-prefix 1000 90 restart 30
!
ip prefix-list OUR-PREFIXES seq 10 permit 198.51.100.0/24
ip prefix-list FROM-ISP-A seq 10 permit 0.0.0.0/0
ip route 198.51.100.0 255.255.255.0 Null0   ! anchors the network statement
```
- **Always filter outbound.** Without `OUR-PREFIXES out` a multihomed site can leak one
  ISP's routes to the other and become transit. RFC 8212 makes "no policy = no routes" the
  default on some newer stacks; IOS classic does not enforce it (behaviour on your
  release unconfirmed).
- `network` only advertises a prefix that exists in the RIB with the exact mask, hence the
  Null0 static.
- `maximum-prefix` protects the router if a peer suddenly sends a full table.

## 5. iBGP between your own edge routers
```
 neighbor 10.255.0.2 remote-as 64512
 neighbor 10.255.0.2 update-source Loopback0
 address-family ipv4 unicast
  neighbor 10.255.0.2 activate
  neighbor 10.255.0.2 next-hop-self
```
Loopbacks must be reachable via OSPF. Without `next-hop-self`, routes from ISP-A carry the
ISP's next hop, which the other router may not know. iBGP needs a full mesh (or route
reflectors) because iBGP-learned routes are not re-advertised to other iBGP peers.

## 6. Steering traffic
Best-path order (simplified): highest weight → highest local-preference → locally
originated → shortest AS path → lowest origin → lowest MED → eBGP over iBGP → lowest IGP
cost to next hop → oldest/lowest router-id.
- **Outbound** (which exit you use): set `local-preference 200` inbound from the preferred ISP
  via route-map.
- **Inbound** (which link others use to reach you): prepend on the backup link
  (`set as-path prepend 64512 64512` outbound). This is a hint, not a guarantee.

After a policy change, `clear ip bgp 203.0.113.1 soft in|out` applies it without
dropping the session.

## Verify
- [ ] `show ip ospf neighbor` shows FULL on every router link and nothing on user VLANs.
- [ ] `show ip ospf interface brief` costs reflect real link speeds.
- [ ] `show ip bgp summary`: sessions Established, received-prefix counts as expected.
- [ ] `show ip bgp neighbors X advertised-routes` lists only your own prefixes.
- [ ] Failover tested: shut the primary link, confirm traffic moves and routes withdraw.
