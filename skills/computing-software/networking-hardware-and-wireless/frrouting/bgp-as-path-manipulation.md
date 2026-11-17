---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-as-path-manipulation
name: bgp-as-path-manipulation
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, as-path, as-path-access-list, prepend, allowas-in, as-override, local-as, regex]
level: advanced
status: docs-checked
description: "Filter and rewrite BGP AS paths in FRR: as-path access-lists, set as-path prepend, replace, exclude, allowas-in, as-override, local-as, regex."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP AS-path manipulation
Lists: `bgp as-path access-list WORD [seq (0-4294967295)] permit|deny LINE`; show with `show bgp as-path-access-list [json]` or `show bgp as-path-access-list WORD [json]`.

Regex tokens: `.` any single character; `*` (0 or more), `+` (1 or more), `?` (0 or 1); `^` start and `$` end of line; `_` matches space, comma, braces, parentheses, or line start/end (AS-value boundaries). Search: `show [ip] bgp regexp LINE`.

Route-map matches: `match as-path WORD`; `match as-path-count MAX_COUNT`.

Route-map sets:
- `set as-path prepend AS-PATH`; `set as-path prepend last-as NUM`.
- `set as-path replace <any|ASN> [<ASN>]`; `set as-path replace as-path-access-list WORD [<ASN>]`.
- `set as-path exclude all`; `set as-path exclude as-path-access-list WORD`.

Per-neighbor:
- `neighbor PEER local-as AS-NUMBER [no-prepend [replace-as [dual-as]]]`
- `neighbor PEER as-override` replaces the peer AS in AS_PATH with the local AS.
- `neighbor PEER allowas-in [<(1-10)|origin>]` accepts routes containing the local AS; with `route-map WORD` only for permitted routes, default count 3.

`bgp bestpath as-path multipath-relax` and `bgp bestpath as-path confed` interact with path length in selection.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the as-path access-list and route-map set/match as-path commands, the BGP Regular Expressions section, local-as, as-override and allowas-in. Fixed: regex token wording and show syntax. Removed: the eBGP-only restriction (not stated in the sources).
Method: documentation only; no commands were run.
