---
id: computing-software.networking-hardware-and-wireless.arista-eos.spanning-tree-mstp
name: spanning-tree-mstp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, spanning-tree, mstp, rstp, portfast]
level: practitioner
status: draft
description: "Configure EOS spanning tree: mode mstp/rapid-pvst, root priority, portfast, BPDU guard and verification."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spanning tree (MSTP default)
Goal: loop prevention with a deterministic root.

```
spanning-tree mode mstp
spanning-tree mst configuration
   name DC1
   revision 1
   instance 1 vlan 100-200
spanning-tree mst 0-1 priority 4096
interface Ethernet10
   spanning-tree portfast
   spanning-tree bpduguard enable
```

```
show spanning-tree
show spanning-tree root
show spanning-tree blockedports
```

- EOS defaults to MSTP on current releases (confirm on yours); the default is spanning tree enabled.
- MST region name, revision and VLAN-instance map must match across switches.
- In leaf-spine L3 designs, STP is minimised or disabled (`spanning-tree mode none`) where no L2 loops exist; do this only deliberately.

Gotcha: two switches with different MST region names are treated as different regions and cause an inconsistent topology. Confirm that name and revision match.

Operational tip: even in an L3 fabric, leave BPDU guard on host ports so a mis-cabled switch cannot become root, and document where STP is intentionally disabled.

## Verify
- `show spanning-tree root` shows the intended switch as the root; `show spanning-tree blockedports` lists only expected ports.
