---
id: computing-software.networking-hardware-and-wireless.bind9.catalog-zones-config
name: catalog-zones-config
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, catalog-zones, catalog, min-update-interval]
level: advanced
status: docs-checked
description: "Configure BIND 9 catalog zones: catalog-zones options, default-primaries, zone-directory, in-memory and min-update-interval."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# catalog zones config
A catalog zone lists member zones, so a secondary needs no per-zone config edits. On the secondary:

```
options {
    catalog-zones {
        zone "catalog.example"
            default-primaries { /* primary addresses */ }
            in-memory no
            zone-directory "catzones"
            min-update-interval 10;
    };
};
zone "catalog.example" {
    type secondary;
    file "catalog.example.db";
    primaries { /* primary addresses */ };
};
```

`default-primaries` is used when a member entry has no primaries property. `zone-directory` is where member zone files go. `in-memory yes` avoids writing them. `min-update-interval` limits how fast catalog updates are processed.

## Checked

2026-11-04. Read the Catalog Zones chapter (Principle of Operation, Configuring Catalog Zones): the catalog-zones example, default-primaries, in-memory, zone-directory and min-update-interval semantics confirmed. Nothing was removed.

Method: documentation only; no commands were run.
