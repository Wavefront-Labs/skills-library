---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-bgp-and-ospf
name: fortigate-bgp-and-ospf
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortigate-bgp, fortios, ospf, bgp-neighbor, router-bgp, route-map, redistribute]
level: practitioner
status: draft
description: "Configure FortiGate BGP and OSPF neighbours, advertised networks, route maps and redistribution, and check adjacencies."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: dynamic routing with an ISP or core.

BGP:
```
config router bgp
    set as 65001
    set router-id 192.0.2.2
    config neighbor
        edit "192.0.2.1"
            set remote-as 64500
            set soft-reconfiguration enable
            set route-map-out "to-isp"
        next
    end
    config network
        edit 1
            set prefix 203.0.113.0 255.255.255.0
        next
    end
end
```
OSPF:
```
config router ospf
    set router-id 192.0.2.2
    config area
        edit 0.0.0.0
        next
    end
    config network
        edit 1
            set prefix 10.1.0.0 255.255.0.0
            set area 0.0.0.0
        next
    end
end
```
Define a route-map and prefix-list for exports so you never leak internal routes to a provider.

Gotchas
- BGP `network` statements only advertise prefixes that exist in the routing table.
- OSPF neighbours stall in ExStart on MTU mismatch; set `set mtu-ignore enable` only as a test.
- Redistribution can create loops; tag redistributed routes and filter on import.

## Verify
```
get router info bgp summary
get router info bgp neighbors 192.0.2.1 advertised-routes
get router info ospf neighbor
get router info routing-table bgp
```
