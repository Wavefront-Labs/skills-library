---
id: computing-software.networking-hardware-and-wireless.juniper-junos.l3vpn
name: l3vpn
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, l3vpn, mpls-vpn, vrf, bgp-vpn]
level: practitioner
status: draft
description: "Configure a Junos PE for a BGP/MPLS Layer 3 VPN with a VRF, route distinguisher/target and MP-BGP."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer 3 VPN basics
Goal: provide L3VPN service to a customer.

```
set routing-instances CUST1 instance-type vrf
set routing-instances CUST1 interface ge-0/0/5.0
set routing-instances CUST1 route-distinguisher 65000:100
set routing-instances CUST1 vrf-target target:65000:100
set routing-instances CUST1 vrf-table-label
set protocols bgp group IBGP-PE family inet-vpn unicast
set protocols bgp group IBGP-PE neighbor 10.255.0.2
set routing-instances CUST1 protocols bgp group CE type external
set routing-instances CUST1 protocols bgp group CE peer-as 65100
set routing-instances CUST1 protocols bgp group CE neighbor 192.0.2.2
```

```
user@host> show route table CUST1.inet.0
user@host> show route table bgp.l3vpn.0
```

- RD makes prefixes unique; route targets control import/export.
- `vrf-table-label` allocates a per-VRF label and enables lookup on egress.

Gotcha: routes in bgp.l3vpn.0 that never reach the VRF mean a route-target mismatch.

Operational tip: use a unique RD per PE per VRF so route reflectors keep every path, while one shared route target per VPN controls membership and import policy.

## Verify
- `show route table CUST1.inet.0` shows remote prefixes with a BGP protocol next-hop; `ping routing-instance CUST1`.
