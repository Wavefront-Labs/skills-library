---
id: computing-software.networking-hardware-and-wireless.arista-eos.port-channel-lacp
name: port-channel-lacp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, port-channel, lacp, channel-group, lag]
level: practitioner
status: draft
description: "Build EOS LACP port-channels with channel-group, lacp mode, and verify member state."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Port-channels and LACP
Goal: aggregate links with LACP.

```
interface Ethernet1-2
   channel-group 10 mode active
interface Port-Channel10
   description to-leaf2
   switchport mode trunk
   port-channel min-links 1
   lacp fallback timeout 90
```

```
show port-channel summary
show lacp neighbor
show port-channel 10 detailed
```

- Modes: `active` (initiates), `passive` (waits), `on` (static, no LACP). Use `active` on both ends.
- `lacp fallback` allows one member to forward before LACP completes (for ZTP/PXE hosts).
- Hash can be adjusted with `port-channel load-balance` (platform specific: confirm).

Gotcha: members must have identical config (speed, switchport mode, VLANs); a mismatch leaves a member suspended. Putting the config on the Port-Channel and not on members is the norm.

Operational tip: use `min-links` equal to the lowest number of members that can carry the traffic, so the bundle goes down cleanly instead of hanging on in a degraded state with congestion.

## Verify
- `show port-channel summary` shows `Po10(U)` with members flagged `P` (in-bundle).
