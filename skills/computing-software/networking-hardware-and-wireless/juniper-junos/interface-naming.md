---
id: computing-software.networking-hardware-and-wireless.juniper-junos.interface-naming
name: interface-naming
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, interface-naming, fpc-pic-port, physical-interfaces, ge-xe-et]
level: practitioner
status: draft
description: "Decode Junos names type-fpc/pic/port, find management and loopback interfaces, and read interface state."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos interface naming and physical interfaces
Goal: read an interface name and know where it lives.

Format: `type-fpc/pic/port[:channel].unit`, for example `xe-0/0/3.0` is 10GE, FPC 0, PIC 0, port 3, unit 0. Types include `ge` (1G), `xe` (10G), `et` (25/40/100G), `ae` (aggregate), `lo0`, `irb`, `vlan`, `fxp0` or `em0`/`me0` (management), `reth` (SRX cluster).

```
user@host> show interfaces terse
user@host> show interfaces xe-0/0/3 extensive | match "error|speed|flap"
user@host> show interfaces diagnostics optics xe-0/0/3
user@host> show chassis hardware | match "PIC|FPC|xcvr"
```

- Switch interface speeds can differ per release/platform: confirm on your model.
- Channelised ports use a colon, for example `et-0/0/48:2`; configure `set chassis fpc 0 pic 0 port 48 channel-speed 25g` (confirm on your platform).

Gotcha: `fxp0`/`em0`/`me0` is out-of-band management and not in the forwarding path; routes pointing at it cause confusing reachability. Do not mix up the physical (`xe-0/0/3`) and the logical (`xe-0/0/3.0`) layers in commands.

## Verify
- `show interfaces terse` lists the interface with Admin/Link `up up`.
