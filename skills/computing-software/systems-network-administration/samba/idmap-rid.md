---
id: computing-software.systems-network-administration.samba.idmap-rid
name: idmap-rid
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-rid, base-rid, rid-backend, idmap, winbind]
level: practitioner
status: docs-checked
description: "Configure the Samba idmap_rid backend: range, base_rid, the RID-to-Unix formula, per-domain disjoint ranges, and the example with a tdb default."
sources:
  - https://www.samba.org/samba/docs/current/man-html/idmap_rid.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap rid
Options:
- `range = low - high`: IDs computed outside it are discarded.
- `base_rid = INTEGER`: default 0 (no RID restriction); SIDs with a lower RID are filtered. Deprecated.

Formulas:
- Unix ID = RID - base_rid + low end of range
- RID = Unix ID + base_rid - low end of range

Rules: each `rid` domain needs an explicit `idmap config` entry, ranges must be disjoint, and `rid` cannot be the default backend; use a writable `tdb` or `ldap` default for BUILTIN, other domains and group mappings.

Example:
```
[global]
security = domain
workgroup = MAIN
idmap config * : backend = tdb
idmap config * : range = 1000000-1999999
idmap config MAIN : backend = rid
idmap config MAIN : range = 10000-49999
idmap config TRUSTED : backend = rid
idmap config TRUSTED : range = 50000-99999
idmap config TRUSTED : base_rid = 500000
```

## Checked
2026-11-04: options, defaults, both formulas, the rules and the example compared with the idmap_rid man page. Removed: an `security = ads` aside and a generic gotcha the page does not state.
Method: documentation only; no commands were run.
