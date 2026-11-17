---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ospf
name: ospf
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ospf, ospf-areas, ospf-neighbor, ospfv2]
level: practitioner
status: draft
description: "Configure Junos OSPF areas, interface types, authentication and read neighbor/database state."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OSPF configuration and troubleshooting
Goal: bring up OSPF adjacencies and diagnose why they fail.

```
set protocols ospf area 0.0.0.0 interface lo0.0 passive
set protocols ospf area 0.0.0.0 interface xe-0/0/3.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface xe-0/0/3.0 authentication md5 1 key "<redacted>"
set protocols ospf area 0.0.0.1 stub no-summaries
set protocols ospf reference-bandwidth 100g
set protocols ospf traceoptions file ospf-trace size 1m files 3
set protocols ospf traceoptions flag error
```

```
user@host> show ospf neighbor
user@host> show ospf interface detail
user@host> show ospf database
user@host> show ospf statistics
```

- Mismatches that block adjacency: area, hello/dead timers, MTU, auth, subnet, stub flag, interface-type.
- `interface-type p2p` avoids DR election on point-to-point Ethernet.
- Junos has no network statement: you enable OSPF per interface, and the interface subnet is advertised.

Gotcha: stuck in `ExStart` almost always means an MTU mismatch. Check `show interfaces ... | match mtu` on both ends.

## Verify
- `show ospf neighbor` state is `Full` and `show route protocol ospf` has the remote prefixes.
