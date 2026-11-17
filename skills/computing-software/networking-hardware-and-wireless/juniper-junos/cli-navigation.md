---
id: computing-software.networking-hardware-and-wireless.juniper-junos.cli-navigation
name: cli-navigation
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, cli-navigation, edit, hierarchy, show-compare]
level: practitioner
status: draft
description: "Move around the Junos configuration hierarchy with edit, up, top and show, and use set/delete/wildcard delete efficiently."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Navigating the configuration hierarchy
Goal: reach any stanza quickly and change it in set or hierarchical form.

```
[edit]
user@host# edit protocols ospf area 0.0.0.0
[edit protocols ospf area 0.0.0.0]
user@host# set interface ge-0/0/1.0 interface-type p2p
user@host# up
user@host# top
user@host# show | compare
user@host# delete protocols ospf area 0.0.0.0 interface ge-0/0/1.0
user@host# wildcard delete interfaces ge-0/0/[2-5]
```

- `edit` changes the current level, `up [n]` goes up, `top` returns to `[edit]`, `exit` leaves a level (and config mode at top).
- `show | compare` diffs the candidate against the committed config; `show | compare rollback 1` diffs against an older one.
- `load set terminal` lets you paste a block of set commands; `load merge` / `load override` load files.
- `copy`, `rename` and `insert` reorder or clone stanzas (important for ordered policy terms).

Gotcha: `set` at a deep `[edit]` level is relative; pasted full-path commands then land in the wrong place. Return to `top` before pasting, or use `load set terminal`.

## Verify
- `show | compare` shows exactly the lines you meant to change and nothing else.
