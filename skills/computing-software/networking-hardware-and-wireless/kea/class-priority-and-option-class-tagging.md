---
id: computing-software.networking-hardware-and-wireless.kea.class-priority-and-option-class-tagging
name: class-priority-and-option-class-tagging
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, client-classes, class-priority, option-data, class-tagging]
level: advanced
status: docs-checked
description: "Predict which class values win in Kea: class order, option precedence against subnet and global scope, and per-option class tagging."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# class priority and option class-tagging
Classes follow configuration order, not alphabetical. Additional classes are ordered by pool, then subnet, then shared network, and within each by their order in `evaluate-additional-classes`.

The server takes the union of class information (options, lease lifetimes, DHCPv4 field values) from all assigned classes. If several classes carry the same item, the first assigned class wins. ALL is always first (highest priority); matching required (additional) classes are last (lowest).

Scope precedence:
- Options in classes override global options and are overridden by options on a subnet, shared network, pool or reservation.
- Lease lifetimes and DHCPv4 field values in classes override global, subnet and shared-network values.

Option class-tagging applies an option value only to members of listed classes, like an if-block in ISC DHCP. Add `client-classes` to the option entry:

```json
"option-data": [ { "client-classes": [ "GROUP1" ],
                   "name": "bar", "data": 123 } ]
```

This lets members of GROUP1 share one value for option foo (set in the class) while getting a subnet-specific value for bar.

## Checked

2026-11-08. Read the Client Classification chapter in full, in particular sections 15.8 Class Priority and 15.9 Option Class-Tagging: class order, first-assigned-wins, ALL first, scope precedence for options versus lifetimes and DHCPv4 fields, and the client-classes option entry. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
