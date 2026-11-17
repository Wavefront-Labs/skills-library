---
id: computing-software.networking-hardware-and-wireless.bind9.rndc-zone-commands
name: rndc-zone-commands
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rndc, zone-management, freeze-thaw]
level: practitioner
status: docs-checked
description: "rndc commands for managing BIND 9 zones: reload, refresh, retransfer, notify, freeze, thaw, sync, addzone, delzone, modzone, showzone."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rndc zone commands
Zone-level `rndc` commands:

- `reload [zone]` reloads zone files; `refresh zone` schedules a refresh; `retransfer zone` retransfers a secondary zone from the primary.
- `notify zone` resends NOTIFY messages.
- `freeze [zone]` suspends dynamic updates so the file can be edited (journal changes are synced into the master file); `thaw` reloads the zone from disk and re-enables updates. `sync [-clean] [zone]` syncs journal changes to the master file; `-clean` also removes the journal.
- `addzone`, `modzone`, `delzone [-clean]` and `showzone` manage zones added at runtime.
- `signing -list|-clear|-nsec3param|-serial`, `sign zone` and `loadkeys zone` control DNSSEC signing.

Editing a dynamic zone: `rndc freeze zone`, edit the file, increment the serial, `rndc thaw zone`.

## Checked

2026-11-04. Confirmed against the rndc man page entries for `reload`, `refresh`, `retransfer`, `notify`, `freeze`, `thaw`, `sync`, `addzone`, `modzone`, `delzone`, `showzone`, `signing`, `sign` and `loadkeys`. Corrected `retransfer`, `freeze`, `thaw` and `sync`.

Method: documentation only; no commands were run.
