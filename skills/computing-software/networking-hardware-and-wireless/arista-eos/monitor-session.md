---
id: computing-software.networking-hardware-and-wireless.arista-eos.monitor-session
name: monitor-session
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, monitor-session, span, port-mirroring, erspan]
level: practitioner
status: draft
description: "Mirror ports with EOS monitor session for packet capture, including remote and tunnel destinations."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Port mirroring (SPAN/ERSPAN)
Goal: capture traffic without disturbing it.

```
monitor session 1 source Ethernet1 both
monitor session 1 destination Ethernet20
monitor session 2 source Ethernet2 rx
monitor session 2 destination Port-Channel30
```

```
show monitor session
show monitor session 1 detail
```

- ERSPAN and GRE tunnel destinations are supported on some platforms: confirm.
- Mirroring to the CPU (`destination cpu`) allows tcpdump via bash.
- Limit with ACLs on source in newer releases (confirm).

Gotcha: mirroring an over-subscribed source to a lower speed destination drops mirrored frames, but not production ones. Do not mirror a 100G port into a 10G destination and trust the capture.

Operational tip: remove monitor sessions after the capture and note them in the change record, because forgotten mirrors consume hardware resources and may expose sensitive traffic. For persistent visibility needs, prefer a packet broker or sFlow rather than keeping SPAN sessions up indefinitely.

## Verify
- `show monitor session` shows `Active`, and a capture on the destination sees packets.
