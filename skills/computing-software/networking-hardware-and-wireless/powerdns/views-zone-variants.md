---
id: computing-software.networking-hardware-and-wireless.powerdns.views-zone-variants
name: views-zone-variants
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, views, zone-variants, split-horizon, networks, lmdb, setting-views]
level: advanced
status: docs-checked
description: "Set up PowerDNS Authoritative views: networks to views, zone variant naming, pdnsutil network and view commands, LMDB requirement."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/views.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Views and zone variants

Experimental since 5.0.0. Needs the LMDB backend, `setting-views` enabled in the configuration, and a non-zero `setting-zone-cache-refresh-interval`.

Model:
- A network (address plus prefix) maps to one view; the smallest matching network wins. The source address, or EDNS subnet, selects it.
- A view holds zone variants, at most one per zone; setting a new one replaces the old.
- For each zone, the view's variant is used if present, otherwise the plain zone. Sources outside every network get ordinary behaviour.

Variant names: `<zone with trailing dot>.<variant>`, such as `example.org..variant01`; the root zone is `..variant`. Variant names allow lowercase letters, digits, `_` and `-`. View names are case sensitive (letters, digits, spaces, `-`, `.`, `_`) and must not start with a dot or space.

Commands:
```
pdnsutil network set <prefix> <view>
pdnsutil network list
pdnsutil view add-zone <view> <variant>
pdnsutil view list-all
pdnsutil view list <view>
```
`view add-zone` does not create the zone; create it first with `zone create`, `zone load`, `zone copy`, etc., which accept variant names.

Advice:
- The page advises hosting all variants on the same backend as the plain zone.
- The packet cache is per view, so multiply `setting-max-packet-cache-entries` by the number of views.
- Catalog producer and consumer zones can have variants; producers are looked up via views but use plain names on the wire. Consumer-side member zones are not given a variant automatically, so they are not scoped to a view.

## Checked

2026-11-08. Read in full: PowerDNS docs views.rst. Confirmed the 5.0.0 experimental note, LMDB and zone-cache requirements, the views setting, variant and view naming rules, smallest-network-wins, one variant per zone per view, the pdnsutil network and view commands, view add-zone not creating zones, per-view packet cache and the catalog zone notes. Added the consumer-side limitation.

Method: documentation only; no commands were run.
