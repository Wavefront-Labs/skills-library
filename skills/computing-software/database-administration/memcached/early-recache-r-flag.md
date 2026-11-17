---
id: computing-software.database-administration.memcached.early-recache-r-flag
name: early-recache-r-flag
category: computing-software
field: database-administration
product: memcached
tags: [early-recache, r-flag, win-flag, ttl, hot-keys]
level: advanced
status: docs-checked
description: "Refresh hot items before they expire using mg R<seconds>: the first client under the threshold gets W, others get Z."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`mg foo v t R30`: if the remaining TTL is below 30 seconds, memcached returns the `W` (win) flag, telling this client to recache the item.

```
mg foo v t R30
VA 2 t29 W
hi
```
The `t` flag returns the remaining TTL. Any further clients see a `Z` flag, meaning a request has already been sent. `R` is similar to and can be combined with `N`.

CAS guard: request `c` as well (`mg foo v c R30` -> `VA 0 c999`) and write with `ms foo 3 C999`, which honors the recache only if the object has not changed since the win token was received.

Purpose: reduce misses on frequently accessed objects. Infrequently accessed objects can be left to expire.

## Checked

2026-11-04. Confirmed against the Meta Text Protocol page ("Early Recache") and protocol.txt (mg R flag, W/Z). Removed: the closing "Pitfall" paragraph about choosing R, which neither page states.

Method: documentation only; no commands were run.
