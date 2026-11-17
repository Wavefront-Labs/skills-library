---
id: computing-software.networking-hardware-and-wireless.bind9.recursion-resource-limits
name: recursion-resource-limits
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, recursive-clients, tcp-clients, fetches-per-zone]
level: advanced
status: docs-checked
description: "Cap BIND 9 recursion resources: recursive-clients, tcp-clients, fetches-per-zone, clients-per-query and related settings."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# recursion resource limits
Resource limits in `options`:

- `recursive-clients`: simultaneous recursive lookups, default 1000.
- `tcp-clients`: simultaneous TCP clients, default 150.
- `fetches-per-zone`: maximum simultaneous iterative queries to any one domain before new queries for it are blocked. Keep it smaller than `recursive-clients`.
- `clients-per-query`: initial minimum number of simultaneous recursive clients for one name, type and class before extra clients are dropped; default 10. named self-tunes it and logs changes.
- `max-cache-size`: cache memory limit.

Inspect live state with `rndc recursing` and `rndc fetchlimit`.

## Checked

2026-11-04. Read the Administrator Reference Manual entries for recursive-clients, tcp-clients, fetches-per-zone, clients-per-query, max-cache-size and the rndc man page entries for recursing and fetchlimit; defaults confirmed. Nothing was removed.

Method: documentation only; no commands were run.
