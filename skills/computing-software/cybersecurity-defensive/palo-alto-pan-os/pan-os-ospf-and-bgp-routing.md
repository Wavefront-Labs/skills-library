---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ospf-and-bgp-routing
name: pan-os-ospf-and-bgp-routing
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [bgp-routing, pan-os, ospf, bgp, dynamic-routing, route-redistribution, bgp-peer, ebgp]
level: practitioner
status: draft
description: "Enable BGP and OSPF on a PAN-OS virtual router with peers, redistribution profiles and CLI checks of neighbour and route state."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/bgp"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: exchange routes with an ISP or core switch and prove adjacencies.

BGP:
```
configure
set network virtual-router default protocol bgp enable yes router-id 192.0.2.2 local-as 65001
set network virtual-router default protocol bgp peer-group ISP type ebgp
set network virtual-router default protocol bgp peer-group ISP peer ISP1 peer-as 64500 local-address interface ethernet1/1 ip 192.0.2.2/24
set network virtual-router default protocol bgp peer-group ISP peer ISP1 peer-address ip 192.0.2.1
set network virtual-router default protocol bgp peer-group ISP peer ISP1 enable yes
commit
```
OSPF:
```
set network virtual-router default protocol ospf enable yes router-id 192.0.2.2
set network virtual-router default protocol ospf area 0.0.0.0 interface ethernet1/2 enable yes metric 10
```

Redistribution: create a redistribution profile (Network > Virtual Routers > Redistribution Profiles) and reference it from the BGP Redistribution Rules, otherwise connected and static prefixes are not advertised.

Gotchas
- Always add explicit export filters to ISP peers so you never become a transit path.
- An MTU mismatch freezes OSPF at ExStart; match MTU on both ends.
- Authentication (MD5) settings must match on both ends.

## Verify
```
show routing protocol bgp summary
show routing protocol bgp peer
show routing protocol bgp loc-rib
show routing protocol ospf neighbor
show routing route type bgp
```
BGP peer state must be Established and OSPF neighbours Full.
