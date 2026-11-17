---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-stp-rstp-mst-root-placement
name: sw-stp-rstp-mst-root-placement
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [stp-root-placement, rstp-mst, bpdu-guard-root-guard, sw-l2-design]
level: practitioner
status: draft
description: "Deploy RSTP/MST with a deliberate root, PortFast, BPDU Guard, Root Guard and loop protection on access ports."
sources:
  - https://www.cisco.com/
  - https://standards.ieee.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spanning tree practice

- Choose the root bridge deliberately (priority low on the distribution/core switch) and a backup root; leaving defaults lets the oldest MAC win.
- Use RSTP (802.1w) or MST (802.1s) instead of legacy STP for fast convergence.
- Access ports: PortFast (edge), BPDU Guard to shut the port if a BPDU arrives. Root Guard on ports where a root should never be learned. Loop Guard/UDLD on point-to-point inter-switch links.
- Storm control on access ports limits broadcast storms.
- Keep Layer 2 domains small; push the routing boundary lower when feasible.

## Verify
- [ ] `show spanning-tree` (or equivalent) shows the intended root and no unexpected blocked paths.
