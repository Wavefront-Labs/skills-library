---
id: computing-software.networking-hardware-and-wireless.juniper-junos.bfd
name: bfd
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, bfd, bfd-liveness-detection, fast-failure-detection]
level: practitioner
status: draft
description: "Add BFD to Junos OSPF, IS-IS, BGP and static routes for sub-second failure detection."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BFD fast failure detection
Goal: detect link/path failure faster than protocol hellos.

```
set protocols ospf area 0 interface xe-0/0/3.0 bfd-liveness-detection minimum-interval 300
set protocols ospf area 0 interface xe-0/0/3.0 bfd-liveness-detection multiplier 3
set protocols bgp group PEERS bfd-liveness-detection minimum-interval 300
set protocols bgp group PEERS bfd-liveness-detection multiplier 3
set routing-options static route 0.0.0.0/0 next-hop 198.51.100.2 bfd-liveness-detection minimum-interval 300
```

```
user@host> show bfd session
user@host> show bfd session extensive
```

- Detection time = interval x multiplier (here about 900 ms).
- Hardware-assisted BFD on some platforms supports lower intervals; software BFD on RE can flap under load: confirm per platform.
- Permit UDP 3784 (and 4784 for multihop) in the lo0 filter.

Gotcha: an aggressive interval on a busy RE causes false positives and route flapping. Also BFD blocked by the loopback filter leaves sessions Down.

Operational tip: start with 300 ms by 3 and tighten only when you have measured RE and line card load; confirm that graceful restart or NSR are tuned with BFD so a switchover does not look like a failure.

## Verify
- `show bfd session` shows `Up` with the intended interval on both ends.
