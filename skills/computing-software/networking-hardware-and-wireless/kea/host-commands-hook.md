---
id: computing-software.networking-hardware-and-wireless.kea.host-commands-hook
name: host-commands-hook
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, libdhcp-host-cmds, reservation-add, operation-target, host-reservations]
level: practitioner
status: docs-checked
description: "Add, query and delete host reservations at runtime with libdhcp_host_cmds: subnet-id rules and the operation-target parameter."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# host commands hook
`libdhcp_host_cmds.so` loads only in kea-dhcp4 or kea-dhcp6. Commands: `reservation-add`, `reservation-get`, `reservation-get-all`, `reservation-get-page`, `reservation-get-by-address`, `reservation-get-by-hostname`, `reservation-get-by-id`, `reservation-del`, `reservation-update`.

`subnet-id`:
- mandatory for most commands;
- optional for `reservation-get-by-hostname` and `reservation-get-by-address`, and for `reservation-get-page`;
- forbidden in `reservation-get-by-id`.
Use 0 for a global reservation.

`operation-target` (optional) selects the data source: `memory` (runtime configuration, volatile until `config-write`), `database`, `all`, or `default` (command-specific). Most commands accept it; the page says `reservation-get-page` does not. By default read commands use all sources; `reservation-add`, `reservation-del` and `reservation-update` use only the database.

`reservation-add` accepts any reservation parameter permitted in the configuration file:

```json
{ "command": "reservation-add", "arguments": { "reservation": {
  "subnet-id": 1, "hw-address": "1a:1b:1c:1d:1e:1f",
  "ip-address": "192.0.2.202" } } }
```

With only the two mandatory entries it assigns no resources to the host. It can also carry `client-id`, `next-server`, `server-hostname`, `boot-file-name`, `option-data` and `client-classes`. Changing the host database requires `hosts-databases` to be configured and not read-only.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM section libdhcp_host_cmds.so (16.14.1 subnet-id, 16.14.2 operation-target, reservation-add examples). Added client-classes and the hosts-databases requirement from the same section.
