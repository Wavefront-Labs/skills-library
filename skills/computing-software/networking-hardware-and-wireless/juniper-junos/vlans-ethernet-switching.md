---
id: computing-software.networking-hardware-and-wireless.juniper-junos.vlans-ethernet-switching
name: vlans-ethernet-switching
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ethernet-switching, vlans, trunk, access-port]
level: practitioner
status: draft
description: "Configure VLANs, access and trunk ports and IRB interfaces on Junos switches using the ELS syntax."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLANs and ethernet-switching (ELS)
Goal: build a basic L2/L3 VLAN setup.

```
set vlans USERS vlan-id 100
set vlans USERS l3-interface irb.100
set interfaces irb unit 100 family inet address 192.0.2.1/24
set interfaces ge-0/0/10 unit 0 family ethernet-switching interface-mode access vlan members USERS
set interfaces xe-0/0/47 unit 0 family ethernet-switching interface-mode trunk vlan members [ USERS VOICE ]
set interfaces xe-0/0/47 native-vlan-id 1
```

```
user@host> show vlans
user@host> show ethernet-switching table
user@host> show ethernet-switching interface
```

- Older non-ELS platforms use `port-mode` and `vlan members`; confirm syntax on your release.
- Each VLAN needs its own `irb` unit for routing; add `vlan-id` unique per VLAN.

Gotcha: VLAN names and IDs are separate; members can be a name or ID, but the trunk dropping a VLAN usually means it was not listed in `members`. Native VLAN mismatch can leak untagged frames.

## Verify
- `show ethernet-switching table` learns MACs in the right VLAN; `ping` from the host to the irb address.
