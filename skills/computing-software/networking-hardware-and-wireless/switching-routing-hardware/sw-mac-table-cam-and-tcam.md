---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-mac-table-cam-and-tcam
name: sw-mac-table-cam-and-tcam
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [switch-tcam-sizing, cam-mac-table, fib-hardware-limits, sw-forwarding-architecture]
level: advanced
status: draft
description: "Explain CAM/TCAM/FIB resources, check utilisation and avoid table exhaustion from ACLs, routes or MAC floods."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware forwarding tables

- Switches forward in ASICs using lookup tables: CAM (exact-match MAC), TCAM (ternary match for ACL/QoS/routing prefixes), and FIB/adjacency tables for routing.
- TCAM is a finite, templated resource. ACL entries, routes, and QoS classes compete; features may not be installed if TCAM is full, and some platforms fall back to slower CPU/software forwarding.
- Many platforms let you choose a template (SDM on Catalyst, similar on others) that favours routes, MACs or ACLs. Changing it often requires a reload.
- Check utilisation with the platform's resource command (e.g. `show platform hardware fed switch active fwd-asic resource tcam utilization` on Catalyst 9000; Junos `show pfe statistics` equivalents). Exact commands vary by platform and release; confirm.
- A MAC flood or very large L2 domain can overflow the MAC table and cause unknown-unicast flooding.

## Verify
- [ ] Utilisation of each table is below a planned headroom (e.g. 70-80 percent) at projected scale.
