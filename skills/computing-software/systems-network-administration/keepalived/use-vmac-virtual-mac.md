---
id: computing-software.systems-network-administration.keepalived.use-vmac-virtual-mac
name: use-vmac-virtual-mac
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, use-vmac, vmac-xmit-base, macvlan, virtual-mac]
level: advanced
status: docs-checked
description: "use_vmac creates a macvlan interface such as vrrp.250 for the VRRP instance; vmac_xmit_base sends VRRP traffic via the physical interface."
sources:
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual MAC (use_vmac)

The software-design page states two items for the VRRP process:
- `use_vmac` creates a macvlan interface (the example name is `vrrp.250`) for the instance.
- `vmac_xmit_base` makes VRRP traffic go out over the physical (base) interface.

The page gives no syntax, defaults or interaction rules beyond this, so confirm placement (inside a `vrrp_instance`) and behaviour against the full configuration reference for your version.

Verify: after start, the macvlan interface exists in the interface listing.

## Checked

2026-11-04. Confirmed use_vmac, the vrrp.250 default naming, the macvlan driver and vmac_xmit_base on the Software Design page. Removed the claim that the interface carries the VIPs, which the page does not state.

Method: documentation only; no commands were run.
