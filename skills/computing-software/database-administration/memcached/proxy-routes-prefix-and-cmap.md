---
id: computing-software.database-administration.memcached.proxy-routes-prefix-and-cmap
name: proxy-routes-prefix-and-cmap
category: computing-software
field: database-administration
product: memcached
tags: [proxy-routes, route-map, cmap, key-prefix, cmdmap]
level: advanced
status: docs-checked
description: "Route by key prefix with map and conf, by command with cmap/cmdmap, and catch-alls with default; the proxy errors without a default."
sources:
  - https://docs.memcached.org/features/proxy/configure/
  - https://docs.memcached.org/features/proxy/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`routes{}` contains `map`, `cmap`, `default`.
- `map = { cust = route_direct{ child = "customer_pool" } }`: prefix routing. Default prefix is everything before the first `/` (`cust/123` -> `cust`).
- `conf = { mode = "prefix" or "anchor", start = "<START>", stop = "<STOP>" }`: change parsing. `prefix` (default) reads from the start of the key to `stop` (default `/`); `anchor` takes the text between `start` (five characters or fewer) and `stop`.
- `cmap = { get = route_allfastest{ children = {"main-1","main-2"} } }`: by command, regardless of prefix.
- `default = ...`: everything else. Without it, unmatched requests return an error.
- `cmdmap{ set = route_direct{...} }` inside a map entry restricts a prefix route to certain commands.

Multiple trees: give `routes{ tag = "main", ... }` and start memcached with one tagged listener per tree, in the form `-l tag_<TAG>_:<HOST>:<PORT>` (for tag `b`, `-l tag_b_:127.0.0.1:12052`); a `routes{}` block with no tag is the default tree.

Verify by sending a `get` through the proxy and checking which backend holds the key.

## Checked

Confirmed against the configure page and reference: routes{} sections map, cmap and default, default prefix rule, conf modes and the five-character start limit, cmap example, the error when default is missing, cmdmap restriction, tag-based route trees. Removed the unconfirmed anchor example key and the claim that stats proxy shows per-command counters; corrected the tagged listener form to the one the examples page uses.

Method: docs-checked 2026-11-09 against docs.memcached.org/features/proxy/configure/ and /reference/ (HTML converted to text and read in full).
