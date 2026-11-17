---
id: computing-software.networking-hardware-and-wireless.juniper-junos.bgp
name: bgp
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, bgp, ebgp, ibgp, bgp-groups]
level: practitioner
status: draft
description: "Configure Junos eBGP/iBGP groups, neighbors, local-as, import/export policy and check session state."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BGP groups, peers and basics
Goal: establish BGP sessions with policy.

```
set routing-options autonomous-system 65001
set protocols bgp group PEERS type external
set protocols bgp group PEERS peer-as 65002
set protocols bgp group PEERS neighbor 198.51.100.2
set protocols bgp group PEERS import IMPORT-PEER
set protocols bgp group PEERS export EXPORT-OWN
set protocols bgp group PEERS authentication-key "<redacted>"
set protocols bgp group PEERS family inet unicast
```

```
user@host> show bgp summary
user@host> show bgp neighbor 198.51.100.2
user@host> show route receive-protocol bgp 198.51.100.2
user@host> show route advertising-protocol bgp 198.51.100.2
```

- iBGP needs a loopback source: `local-address 10.255.0.1` plus an IGP, and `multihop` for non-adjacent eBGP.
- Without policies, eBGP import accepts everything; export advertises BGP routes only (never statics/directs).
- Apply `family inet6 unicast` or `evpn signaling` per group as needed.

Gotcha: iBGP does not re-advertise iBGP routes; use route reflectors (`cluster`) or a full mesh.

## Verify
- `show bgp summary` shows `Establ` with nonzero received prefixes.
