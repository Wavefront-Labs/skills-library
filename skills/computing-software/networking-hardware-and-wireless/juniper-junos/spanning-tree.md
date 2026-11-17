---
id: computing-software.networking-hardware-and-wireless.juniper-junos.spanning-tree
name: spanning-tree
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, spanning-tree, rstp, mstp, vstp]
level: practitioner
status: draft
description: "Configure Junos RSTP/MSTP/VSTP, bridge priority, edge ports, BPDU and loop protection."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RSTP, MSTP and VSTP
Goal: avoid L2 loops with a deterministic root.

```
set protocols rstp bridge-priority 4k
set protocols rstp interface xe-0/0/47 mode point-to-point
set protocols rstp interface ge-0/0/10 edge
set protocols rstp bpdu-block-on-edge
set protocols mstp configuration-name REGION1
set protocols mstp bridge-priority 4k
set protocols vstp vlan 100 bridge-priority 8k
```

```
user@host> show spanning-tree bridge
user@host> show spanning-tree interface
```

- Priorities are multiples of 4096.
- `edge` ports skip the listening/learning delay but must not receive BPDUs; combine with `bpdu-block-on-edge`.
- `loop-protect`/`bpdu-loop-guard` mitigates unidirectional failures.

Gotcha: leaving priority at default means any new switch might become root. Set the intended root and backup explicitly. Which protocol is enabled by default varies by platform: confirm.

Operational tip: document which switch is the root and backup root, and verify with `show spanning-tree bridge` after any topology change or new switch insertion in the access layer.

## Verify
- `show spanning-tree bridge` shows this switch as `Root ID` match on the intended root and port roles are as designed.
