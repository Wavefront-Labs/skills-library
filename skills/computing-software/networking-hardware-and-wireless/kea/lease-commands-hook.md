---
id: computing-software.networking-hardware-and-wireless.kea.lease-commands-hook
name: lease-commands-hook
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, libdhcp-lease-cmds, lease4-add, lease4-del, lease-management]
level: practitioner
status: docs-checked
description: "Manage Kea leases at runtime with libdhcp_lease_cmds: lease4-add, lease6-add, get-by queries and lease deletion by address or identifier."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lease commands hook
`libdhcp_lease_cmds.so` is open source and loadable only by kea-dhcp4 or kea-dhcp6. Use cases: migrating between servers, retiring a network, removing a device known not to return, and automating monitoring. Since Kea 2.7.7 it also supports binding variables, custom per-lease values.

- `lease4-add` needs an IPv4 address and an identifier (hw-address); `lease6-add` needs an IPv6 address, `iaid` and `duid`. `subnet-id` is optional; if absent or 0, Kea runs subnet selection, and if given it must match an existing subnet. `lease6-add` also adds prefix leases: give `type` "IA_PD", `prefix-len` and `subnet-id` (Kea cannot guess subnet-id for prefixes), with the prefix in `ip-address`. Optional parameters include `valid-lft`, `expire`, `hostname`, `state` (0 default, 1 declined, 2 expired-reclaimed, 3 released) and `user-context`.

```json
{ "command": "lease4-add", "arguments": {
  "ip-address": "192.0.2.202", "hw-address": "1a:1b:1c:1d:1e:1f" } }
```

- `lease4-get-by-*` / `lease6-get-by-*` return all leases matching hw-address (IPv4), client-id (IPv4), duid (IPv6) or hostname, in the `lease4-get-all` format; the list can be empty.
- `lease4-del` / `lease6-del` delete by address, or by `subnet-id`, `identifier-type` ("hw-address", "client-id" for v4; "duid" for v6) and `identifier` (v6 also type and IAID).

Others in the library: `lease6-bulk-apply`, `lease4-get`, `lease4-get-all`, `lease4-get-page`, `lease4-update`, `lease4-wipe`, `lease4-resend-ddns`, `lease4-write`.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM section libdhcp_lease_cmds.so (16.15.1 to 16.15.11 and the command list, 2.7.7 binding variables, use cases). Added the prefix lease parameters and state codes from 16.15.1. Nothing removed.
