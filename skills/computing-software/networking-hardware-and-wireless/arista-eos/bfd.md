---
id: computing-software.networking-hardware-and-wireless.arista-eos.bfd
name: bfd
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, bfd, bidirectional-forwarding, fast-detection]
level: practitioner
status: draft
description: "Enable BFD on EOS interfaces and BGP/OSPF neighbors for fast failure detection."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BFD
Goal: detect path failures quickly.

```
interface Ethernet1
   bfd interval 300 min-rx 300 multiplier 3
router bgp 65101
   neighbor SPINES bfd
router ospf 1
   bfd default
```

```
show bfd peers
show bfd peers detail
```

- Detection time = min-rx * multiplier (about 900 ms here).
- Hardware-offloaded BFD on many platforms supports lower timers; check platform guidance.
- Set the same timers on both peers.

Gotcha: aggressive timers combined with a busy CPU or a service ACL/CoPP that drops UDP 3784 cause session flaps.

Operational tip: when adding BFD across a fabric, roll it out per tier and compare flap counters in `show bfd peers detail` before and after to prove it does not add instability. Remember that BFD sessions count against a platform limit, so check the supported session scale in the datasheet before enabling it everywhere.

## Verify
- `show bfd peers` lists the session `Up` with the configured intervals.
