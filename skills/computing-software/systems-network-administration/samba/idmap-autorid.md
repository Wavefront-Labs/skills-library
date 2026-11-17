---
id: computing-software.systems-network-administration.samba.idmap-autorid
name: idmap-autorid
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-autorid, rangesize, autorid, idmap, winbind]
level: advanced
status: docs-checked
description: "Configure the Samba idmap_autorid backend: range and rangesize rules, defaults, ID formulas, and a minimal and a large example."
sources:
  - https://www.samba.org/samba/docs/current/man-html/idmap_autorid.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap autorid
Options and defaults:
- `range = low - high`: should be a multiple of `rangesize` and at least twice it (the mandatory BUILTIN domain needs space).
- `rangesize`: default 100000, minimum 2000. RIDs above it spill into extension ranges.
- `read only`: default `no`; `yes` blocks new ranges and mappings.
- `ignore builtin`: default `no`.

Formulas (range number is stored in `autorid.tdb`):
- Unix ID = (RID % RANGE SIZE) + LOW + RANGE NUMBER x RANGE SIZE
- Reduced RID = RID % RANGE SIZE; the domain range index = RID / RANGE SIZE.
- One range is used for local users and groups and well-known SIDs, so `rangesize` also limits how many local users and groups can be created.
- The domain-to-range mapping is stored in `autorid.tdb`; back it up regularly.

Minimal:
```
[global]
security = ads
workgroup = CUSTOMER
realm = CUSTOMER.COM
idmap config * : backend = autorid
idmap config * : range = 1000000-1999999
```
Large, with an SFU trusted domain on a non-overlapping range:
```
idmap config * : backend = autorid
idmap config * : range = 1000000-19999999
idmap config * : rangesize = 1000000
idmap config TRUSTED : backend = ad
idmap config TRUSTED : range = 50000-99999
idmap config TRUSTED : schema_mode = sfu
```
Idmap and SFU ranges must not overlap.

## Checked
2026-11-04: options, defaults, formulas and both examples compared with the idmap_autorid man page. Removed: a worked RID example and slot-count arithmetic the page does not give, and a claimed absence of a range default.
Method: documentation only; no commands were run.
