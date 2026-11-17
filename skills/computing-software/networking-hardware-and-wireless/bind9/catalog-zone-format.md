---
id: computing-software.networking-hardware-and-wireless.bind9.catalog-zone-format
name: catalog-zone-format
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, catalog-zone-format, ptr, apl]
level: advanced
status: docs-checked
description: "Catalog zone content for BIND 9: version TXT record, member PTR records under zones, and custom properties such as primaries, allow-query and coo."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# catalog zone format
The catalog zone is an ordinary zone containing:

```
version.catalog.example. IN TXT "2"
<label>.zones.catalog.example. IN PTR domain.example.
```

Schema versions 1 and 2 are supported. Each member is a PTR record under `zones` whose target is the member zone name.

Custom properties go under the member label. `primaries` gives per-member primaries (a TSIG key can be attached through a TXT record). `allow-query` and `allow-transfer` are given by APL records. With schema version 2 these sit under an `ext` label.

The `coo` property hands a member to another catalog (change of ownership).

## Checked

2026-11-04. Confirmed against the ARM catalog zones section (chapter 6): `version.<catalog>` TXT record, schema versions 1 and 2, PTR members under `zones`, custom properties, `ext` label for version 2, `primaries` with TSIG TXT, APL records for `allow-query` and `allow-transfer`, `coo`. Nothing removed.

Method: documentation only; no commands were run.
