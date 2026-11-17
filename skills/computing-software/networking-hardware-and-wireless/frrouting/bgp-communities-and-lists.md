---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-communities-and-lists
name: bgp-communities-and-lists
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, community, community-list, well-known-communities, blackhole, send-community, alias]
level: practitioner
status: docs-checked
description: "Match and set standard BGP communities in FRR: well-known values, community-list standard and expanded, send-community, aliases, route-map match and set, and show by community."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP communities and lists
Format `AS:VAL` (4 octets). Well-known: `graceful-shutdown` 65535:0, `accept-own` 65535:1, `llgr-stale` 65535:6, `no-llgr` 65535:7, `blackhole` 65535:666 (receiver adds NO_ADVERTISE), `no-export` 0xFFFFFF01, `no-advertise` 0xFFFFFF02, `local-AS` 0xFFFFFF03, `no-peer` 65535:65284.

Lists:
- `bgp community-list standard NAME permit|deny COMMUNITY` (empty COMMUNITY matches all).
- `bgp community-list expanded NAME permit|deny COMMUNITY` is a regex filter, not usable for set.
- Numbered: `(1-99)` standard, `(100-500)` expanded. The un-typed `bgp community-list NAME ...` is deprecated since 5.0.
- `bgp community alias NAME ALIAS`; `show bgp community-list [NAME detail]`.

Route-map:
- `match community WORD [exact-match]`, `match community-limit (0-65535)`, `match alias WORD`.
- `set community <none|COMMUNITY> additive` (replace or append; `none` suppresses), `set comm-list <delete|add|replace> WORD`.

Sending: `neighbor PEER send-community <both|all|extended|standard|large>` (default enabled).

Show: `show [ip] bgp <ipv4|ipv6> [all] community COMMUNITY [exact-match] [wide|json]` and `show [ip] bgp <ipv4|ipv6> community-list WORD [exact-match] [json]`.

## Checked

2026-11-04. Confirmed against the FRR BGP page: well-known community values, community-list standard and expanded, numbered lists, deprecation of the untyped form since 5.0, aliases, route-map match and set forms, send-community default. Corrected the show-by-community syntax (COMMUNITY is required; community-list takes json, not wide).
Method: documentation only; no commands were run.
