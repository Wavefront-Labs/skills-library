---
id: computing-software.networking-hardware-and-wireless.unbound.views-per-client-zones
name: views-per-client-zones
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, view, access-control-view, view-first, split-horizon, interface-view]
level: advanced
status: docs-checked
description: "Give client groups their own local-zone trees in Unbound with view clauses, access-control-view and view-first, plus runtime view commands."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/tags-views.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# views per client zones
A `view:` clause has a unique `name:` and its own `local-zone`, `local-data` and `local-data-ptr` (plus `response-ip` and `response-ip-data`, which need `respip`). Views suit many clients that each have their own zones.

```
view:
    name: "guests"
    local-zone: internal.example static
access-control-view: 192.168.20.0/24 guests
```

Map clients with `access-control-view` (netblock) or `interface-view` (interface).

View options override the global ones. A client in a view that defines local zones uses only that view's zone tree; with at least one view `local-zone` and `view-first: no`, the default local zones are added to the view (disable one with `nodefault`). If the view has no `local-zone`, the global local zones apply. `view-first: yes` (default no) checks the view first, then the global tree. A zone of type `noview` breaks out of the view to the global local zones. Options from `unbound.conf` other than the view-specific ones keep their global value.

Runtime: `view_list_local_zones`, `view_local_zone view name type`, `view_local_zone_remove`, `view_list_local_data`, `view_local_data`, `view_local_data_remove`, `view_local_datas` and `view_local_datas_remove`, each mirroring its non-view command.

## Checked

2026-11-08. Read the Tags and Views topic page, the View Options section of unbound.conf and the view_* unbound-control commands. Corrected the claim that a view always ignores global config: the global local zones apply when the view has no local-zone, and default zones are added to a view that has one.

Method: documentation only; no commands were run.
