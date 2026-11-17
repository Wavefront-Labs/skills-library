---
id: computing-software.networking-hardware-and-wireless.unbound.local-zone-types
name: local-zone-types
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, local-zone, static, transparent, redirect, always-nxdomain, blocking]
level: practitioner
status: docs-checked
description: "Pick the right local-zone type in Unbound for overrides and blocking: static, transparent, redirect, the always_ types, block_a and the inform variants."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local zone types
`local-zone: <name> <type>` decides the answer when `local-data` has no exact match.

- `deny` drops, `refuse` replies REFUSED; local data still answers if matched.
- `static` answers from local data, else NODATA or NXDOMAIN (with apex SOA if present).
- `transparent` answers from local data, other names resolve normally; a name with data but not the type gets NODATA. `typetransparent` resolves other types normally.
- `redirect` answers the zone and all subdomains from local data; a single apex CNAME is supported.
- `inform`, `inform_deny`, `inform_redirect` act like transparent, deny and redirect but log client IP and query.
- `always_transparent`, `always_refuse` (also blocks DS at the apex), `always_nxdomain`, `always_nodata`, `always_deny` ignore local data. `always_null` returns 0.0.0.0 or :: for every name.
- `block_a` / `block_aaaa` resolve all types but give NODATA for A or AAAA; `_wdata` variants use local data if present.
- `nodefault` disables default content for that zone; `noview` escapes the current view.

Add at runtime with `unbound-control local_zone name type`.

## Checked

2026-11-08. Read the local-zone option and every type description in the unbound.conf manual in full. Fixed inform, inform_deny and inform_redirect, which behave like transparent, deny and redirect plus logging (the draft said normal).

Method: documentation only; no commands were run.
