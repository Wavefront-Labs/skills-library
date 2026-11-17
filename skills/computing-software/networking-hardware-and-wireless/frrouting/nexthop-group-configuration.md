---
id: computing-software.networking-hardware-and-wireless.frrouting.nexthop-group-configuration
name: nexthop-group-configuration
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, nexthop-group, backup-group, resilient, weight, label, vni]
level: advanced
status: docs-checked
description: "Define named FRR nexthop groups with nexthop entries, labels, VNI, weights, backup indexes and resilient bucket settings that need Linux 5.19 or newer."
sources:
  - https://docs.frrouting.org/en/latest/nexthop_groups.html
  - https://docs.frrouting.org/en/latest/pbr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nexthop group configuration
- `nexthop-group NAME` creates a group and enters a sub-mode; exit with `exit` or `end`.
- `backup-group NAME` names a group whose nexthops serve as backups for this group.
- `nexthop [A.B.C.D|X:X::X:X] [INTERFACE [onlink]] [nexthop-vrf NAME] [label LABELS] [vni VNI] [weight WEIGHT] [backup-idx INDEXES]`. Address, interface, `onlink` and `nexthop-vrf` match static route nexthops.
  - `label`: 16-1048575, separate multiple with `/`; labels 0-15 are reserved; maximum 16.
  - `vni`: 1-16777215.
  - `weight`: 1-4294967295, for ECMP load balancing.
  - `backup-idx`: 0-254, separate multiple with `,`.
- `resilient buckets (1-256) idle-timer (1-4294967295) unbalanced-timer (1-4294967295)` creates a resilient group; timers are in seconds. Buckets for a lost nexthop are reassigned instead of using normal kernel hashing. It must currently be the first command entered and requires Linux kernel 5.19 or newer.

The page gives no default values for these parameters. The PBR page uses nexthop groups through `set nexthop-group NAME` in a pbr-map and shows them with `show pbr nexthop-groups [NAME] [json]`.

## Checked

2026-11-08. Read the FRR Nexthop Groups page (command forms, parameter ranges, resilient group requirements) and the PBR page (nexthop-group use and show command). Nothing else changed.
Method: docs-only read of cited pages, 2026-11-08
