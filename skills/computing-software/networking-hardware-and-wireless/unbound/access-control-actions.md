---
id: computing-software.networking-hardware-and-wireless.unbound.access-control-actions
name: access-control-actions
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, access-control, refuse, allow, allow-snoop, netblock]
level: practitioner
status: docs-checked
description: "Decide which client netblocks may query Unbound using access-control and its actions: deny, refuse, allow, allow_setrd, allow_snoop, allow_cookie and the non_local variants."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access control actions
`access-control: <netblock> <action>`. By default everything is refused except 127.0.0.0/8. The most specific matching netblock is used; if none match, refuse is used.

Actions:
- `deny` silently drops queries; `refuse` returns REFUSED.
- `allow` permits recursive queries; non-recursive queries are refused except for authoritative local-data (and non-recursive requests for cached data are refused).
- `allow_setrd` ignores the RD bit and treats every request as recursion-desired (violates RFC 1034); the page says it helps when another server forwards to Unbound with RD cleared.
- `allow_snoop` allows recursive and non-recursive queries; the page warns it enables cache snooping but is useful for debugging cache contents.
- `allow_cookie` accepts UDP queries only with a valid DNS Cookie (needs `answer-cookie`); client-cookie-only or invalid cookies get BADCOOKIE, cookie-less UDP gets REFUSED with TC set. Stateful transports are accepted regardless of cookies.
- `deny_non_local` and `refuse_non_local` allow authoritative local-data only, dropping or refusing everything else respectively.

Related: `access-control-tag` assigns tags to a netblock (creating an implicit allow if there is no entry), `access-control-tag-action` sets the action per tag (the first matching tag in `define-tag` order wins), `access-control-tag-data` sets redirect RR data per tag, and `access-control-view` sets a view. `interface-action` works like access-control per interface (default refuse; the interface must already be defined) and any access-control option overrides it for the same clients.

## Checked
Method: 2026-11-08 read the unbound.conf manual access-control, tag, view and interface-action entries. The default (only 127.0.0.0/8 allowed) and most-specific-match claims were already correct; added per-action and tag details.
