---
id: computing-software.networking-hardware-and-wireless.bind9.zone-types-overview
name: zone-types-overview
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, zone-types, primary, secondary]
level: practitioner
status: docs-checked
description: "BIND 9 zone types at a glance: primary, secondary, mirror, hint, stub, static-stub, forward and redirect, and what each does."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zone types overview
Zone `type` values:

- `primary`: loads data from a file (or via dynamic update).
- `secondary`: transfers from `primaries`.
- `mirror`: a secondary whose contents are DNSSEC-validated before use; for the root and similar.
- `hint`: initial root server list (zone ".").
- `stub`: transfers only the NS records of a zone.
- `static-stub`: fixed `server-addresses` or `server-names` for a zone.
- `forward`: forwards queries for the zone.
- `redirect`: supplies answers when normal resolution would return NXDOMAIN; one redirect zone per view. The separate `nxdomain-redirect` option is the deprecated one.

Top-level `template` blocks hold zone options that zones reference with `template`; options set in the zone override the template. A template cannot contain `in-view` or `template`. The manual's example names templates `primary` and `secondary`.

## Checked

2026-11-04. Confirmed against the ARM zone block, `type redirect` and Zone Templates entries. Corrected the redirect deprecation wording and the template description.

Method: documentation only; no commands were run.
