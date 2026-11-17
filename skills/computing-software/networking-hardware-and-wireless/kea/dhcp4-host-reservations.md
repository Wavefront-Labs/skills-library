---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-host-reservations
name: dhcp4-host-reservations
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, host-reservations, hw-address, circuit-id, client-id]
level: practitioner
status: docs-checked
description: "Create DHCPv4 host reservations in a subnet by hw-address, duid, circuit-id or client-id, with address and hostname; in-pool versus out-of-pool."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 host reservations
Reservations are an array under a subnet (`reservations`). Each element has one identifier plus optional data.

```json
"reservations": [
  { "hw-address": "1a:1b:1c:1d:1e:1f", "ip-address": "192.0.2.202" },
  { "duid": "0a:0b:0c:0d:0e:0f", "ip-address": "192.0.2.100",
    "hostname": "alice-laptop" },
  { "circuit-id": "'charter950'", "ip-address": "192.0.2.203" },
  { "client-id": "01:11:22:33:44:55:66", "ip-address": "192.0.2.204" } ]
```

- The reserved address must be inside the subnet. In-pool and out-of-pool reservations use the same syntax.
- Use as few identifier types as possible, preferably one.
- Hostnames should be unique if DNS updates are planned.
- A mobile host needs a separate definition in each subnet it may visit; two definitions with the same hardware address in one subnet are not allowed.
- A reservation can also carry a hostname, options, the message fields `siaddr`, `sname` and `file`, and client classes.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Host Reservation in DHCPv4 and Address Reservation Types (partial read, those sections in full). Confirmed the identifiers, subnet-membership rule, one-type advice, unique hostnames and the mobile host rule. Corrected: the draft named next-server, server-hostname and boot-file-name as reservation fields; the section documents the message fields siaddr, sname and file, plus hostname, options and client classes, so the list was reworded.

Method: documentation only; no commands were run.
