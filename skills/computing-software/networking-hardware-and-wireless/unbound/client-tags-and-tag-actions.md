---
id: computing-software.networking-hardware-and-wireless.unbound.client-tags-and-tag-actions
name: client-tags-and-tag-actions
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, define-tag, access-control-tag, local-zone-tag, per-client-filtering, local-zone-override]
level: advanced
status: docs-checked
description: "Give different clients different answers in Unbound with define-tag, access-control-tag, interface-tag, local-zone-tag and tag-action overrides."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/tags-views.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client tags and tag actions
1. `define-tag: "ads social"` lists tag names in one quoted string.
2. Tag clients with `access-control-tag: <netblock> "<tags>"` or listening interfaces with `interface-tag`.
3. Tag zones with `local-zone-tag`.
4. Optionally vary behaviour with `access-control-tag-action` / `interface-tag-action` (a local-zone type per client and tag) and `access-control-tag-data` / `interface-tag-data` (local-data per client and tag).

```
define-tag: "ads social"
access-control-tag: 192.168.10.0/24 "ads"
local-zone: tracker.example refuse
local-zone-tag: tracker.example "ads"
access-control-tag-action: 192.168.10.0/24 "ads" deny
```

Precedence:
- `access-control*` overrides `interface-*` for the clients it targets.
- An interface used with `interface-tag*` must already be listed with `interface:`.
- With several tags, the action or data is looked up using the first tag shared by the client and the zone, in `define-tag` order.
- A tag entry whose block matches no access-control rule creates one with type allow.
- A tagged zone applies if at least one tag matches; untagged zones apply to everyone; the most specific matching zone is chosen.
- Zone type comes from the matching zone unless a tag-action overrides it.
- `local-zone-override` beats tagged and untagged types and tag actions.

Tags are stored as bitmaps, so keep their number small; use views for many clients with their own zones.

## Checked

2026-11-08. Read the Tags and Views topic page and the define-tag, access-control-tag*, interface-tag* and local-zone-tag entries of the unbound.conf manual. Added two details from the manual: the interface must already be listed with interface, and the action lookup uses the first shared tag in define-tag order.

Method: documentation only; no commands were run.
