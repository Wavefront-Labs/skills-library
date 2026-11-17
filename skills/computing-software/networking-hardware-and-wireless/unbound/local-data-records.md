---
id: computing-software.networking-hardware-and-wireless.unbound.local-data-records
name: local-data-records
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, local-data, local-data-ptr, split-horizon, overrides, txt-records]
level: intro
status: docs-checked
description: "Serve custom DNS records from Unbound with local-data and local-data-ptr, and how they interact with the enclosing local-zone."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local data records
`local-data:` takes one resource record as a string. Matching is exact unless the enclosing zone is `redirect`. Use single quotes for TXT records. Data outside any local zone creates a `transparent` zone for it, so other names keep resolving normally.

`local-data-ptr: "IPaddr name"` is shorthand for the PTR record, with an optional TTL.

Zone type controls everything not matched: in a `static` zone a missing name or type gets NODATA or NXDOMAIN; in `transparent` it resolves normally. See local-zone-types.

Runtime control:
- `local_data RR data` adds a record (creating a transparent zone if none covers it).
- `local_data_remove name` removes all data for the name, or one RR if given.
- `local_datas` and `local_datas_remove` bulk add or remove from stdin, one per line.
- `list_local_data` shows the current records.

Runtime changes are not written to the config file; the manual says so for set_option and the insecure and forward commands, and a reload reads the config fresh.

`access-control: allow` refuses non-recursive queries except for static local-data.

## Checked

2026-11-08. Read local-data, local-data-ptr, access-control allow and the unbound-control local_data family. Commands confirmed. Replaced the unsupported blanket statement that runtime changes never reach the config file with what the manual actually says.

Method: documentation only; no commands were run.
