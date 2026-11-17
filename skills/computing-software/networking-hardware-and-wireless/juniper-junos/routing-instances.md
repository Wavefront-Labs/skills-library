---
id: computing-software.networking-hardware-and-wireless.juniper-junos.routing-instances
name: routing-instances
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, routing-instances, virtual-router, vrf, instance-type]
level: practitioner
status: draft
description: "Create Junos virtual-router and VRF routing instances, name the RIB, and import/export routes between instances."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing instances and RIBs
Goal: separate routing tables (management VRF, tenants).

```
set routing-instances MGMT instance-type virtual-router
set routing-instances MGMT interface fxp0.0
set routing-instances MGMT routing-options static route 0.0.0.0/0 next-hop 192.0.2.254
set routing-instances CUST1 instance-type vrf
set routing-instances CUST1 route-distinguisher 65000:1
set routing-instances CUST1 vrf-target target:65000:1
set routing-options rib-groups LEAK import-rib [ inet.0 MGMT.inet.0 ]
```

- Table names are `<instance>.inet.0`, `.inet6.0`, `.mpls.0`; the default is `inet.0`.
- Commands take the instance: `ping 192.0.2.1 routing-instance MGMT`, `show route table MGMT.inet.0`.
- `instance-import`/`instance-export` policies or `rib-groups` leak routes between instances.

Gotcha: forgetting `routing-instance` on ping/traceroute/ssh is the classic reason "it works from inet.0 but not the VRF." Also, an interface can be in only one instance.

Operational tip: name instances after their purpose (MGMT, CUST-A) and document RD and route-target numbering so imports and exports stay predictable as the number of VRFs grows.

## Verify
- `show route instance` lists the instance with its interfaces.
- `ping ... routing-instance MGMT` works.
