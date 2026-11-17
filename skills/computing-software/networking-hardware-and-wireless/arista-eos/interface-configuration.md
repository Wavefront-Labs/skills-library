---
id: computing-software.networking-hardware-and-wireless.arista-eos.interface-configuration
name: interface-configuration
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, interface-config, ethernet-interface, routed-port, switchport]
level: practitioner
status: draft
description: "Configure EOS Ethernet interfaces as switchports or routed ports, speed, MTU, descriptions and status checks."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interface configuration
Goal: put an interface into a known, documented state.

```
interface Ethernet1
   description to-spine1
   no switchport
   ip address 198.51.100.1/31
   mtu 9214
   speed forced 100gfull
   no shutdown
interface Ethernet10
   description server-a
   switchport mode access
   switchport access vlan 100
```

```
show interfaces status
show interfaces Ethernet1 counters errors
show interfaces Ethernet1 transceiver
show interfaces Ethernet1 | include MTU
```

- Default for most ports is switchport; `no switchport` makes a routed port.
- `mtu 9214` is the typical max on many platforms; confirm for your model.
- `show interfaces status` gives the quick state, and `errdisabled` ports appear there.

Gotcha: setting `speed forced` without matching the optic or peer leads to link down. Configure `speed auto` or break-out ports with the right module per platform.

Operational tip: always set `description` with the far-end device and port, because it is the first thing read during an outage. Consider `load-interval 30` for faster rate counters while troubleshooting.

## Verify
- `show interfaces status` shows `connected` and the intended speed; `ping 198.51.100.0` works for routed ports.
