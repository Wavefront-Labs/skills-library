---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-junos-operational-commands-and-filters
name: nda-junos-operational-commands-and-filters
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [junos-operational-mode, junos-firewall-filter, junos-pipe-filters, nda-junos-ops]
level: practitioner
status: draft
description: "Navigate Junos operational vs configuration mode, use pipes (match, count, display set) and write firewall filters for the control plane."
sources:
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos operations

- Operational mode (`>`) for show/monitor; configuration mode (`#`) via `configure`. Run operational commands from config mode with `run show ...`.
- Pipes: `| match`, `| except`, `| count`, `| display set`, `| display json`, `| compare`, `| no-more`. `show configuration | display set` produces copyable commands.
- `monitor traffic interface ge-0/0/0 no-resolve` captures on the RE-facing path; `show interfaces terse` is the quick status view.
- Firewall filters (the Junos ACL) apply per family and direction on interfaces; protect the routing engine with a filter on `lo0` (control plane) allowing only required management and routing protocols.
- Use apply-groups and `show | display inheritance` to understand effective config.

## Verify
- [ ] The lo0 filter counters increment for expected traffic and drop counters stay low for legitimate sources.
