---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.virtual-server-types
name: virtual-server-types
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, virtual-server, standard-virtual, forwarding-ip, performance-l4]
level: practitioner
status: draft
description: "Choose and create BIG-IP standard, forwarding (IP), performance (layer 4) and reject virtual servers with tmsh."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual server types: standard, forwarding, performance

```
tmsh create ltm virtual vs_web destination 10.1.10.100:443 ip-protocol tcp pool pool_web profiles add { tcp { } http { } clientssl { context clientside } } source-address-translation { type automap }
tmsh create ltm virtual vs_fwd destination 0.0.0.0:any mask any ip-forward vlans-enabled vlans add { internal }
tmsh create ltm virtual vs_l4 destination 10.1.10.101:80 ip-protocol tcp profiles add { fastL4 } pool pool_web
tmsh create ltm virtual vs_deny destination 10.1.10.0/24:any reject
```
- Standard: full proxy, supports any profile (HTTP, SSL, OneConnect), full iRules.
- Forwarding (IP): routes packets, no pool; use for pass-through traffic and with `translate-address disabled`.
- Performance (Layer 4) uses the `fastL4` profile: no L7 events, iRules limited to L4 events; hardware offload possible (PVA/ePVA, confirm on platform).
- Performance (HTTP) is a fast HTTP proxy with a restricted feature set.
- Reject refuses matching traffic with a TCP RST / ICMP unreachable.
- A virtual matches the most specific destination first (host over network over wildcard), then the more specific port; use `tmsh show ltm virtual-address` to see the address list.
- `vlans-enabled` plus a `vlans` list restricts the VS to those ingress VLANs; omit it and the VS answers on all VLANs.
- Gotcha: `translate-address disabled` and `translate-port disabled` are needed for forwarding VSs; with translation on, destination gets rewritten.

Verify: `tmsh show ltm virtual vs_web` shows `Availability: available` and rising client-side connections, and `tmsh show ltm virtual-address`.
