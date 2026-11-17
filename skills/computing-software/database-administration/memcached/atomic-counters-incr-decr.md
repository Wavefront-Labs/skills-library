---
id: computing-software.database-administration.memcached.atomic-counters-incr-decr
name: atomic-counters-incr-decr
category: computing-software
field: database-administration
product: memcached
tags: [incr, decr, counter, atomic, 64-bit]
level: practitioner
status: docs-checked
description: "Use incr and decr (or ma) for atomic counters: key must exist, values are unsigned 64-bit, decr floors at 0, incr wraps."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```
incr <key> <value> [noreply]
decr <key> <value> [noreply]
```
- The item must already exist; these commands do not treat a missing key as 0, they fail. Reply `NOT_FOUND` on a miss, else the new value.
- The stored data is treated as the decimal form of a 64-bit unsigned integer; if it is not, the command returns an error.
- `decr` below 0 gives 0; `incr` wraps around the 64-bit mark.
- A number that loses length when decremented may come back space-padded; do not rely on that.

Meta arithmetic `ma` replaces incr/decr:
```
ma key N0 J10 D5 v        auto-create on miss with initial 10, add 5, return value
ma key MD D1              decrement (M modes: I or + increment, D or - decrement)
```
`N<ttl>` auto-creates the item on a miss, `J` is the initial value on a miss (must be combined with N; default 0), `D` is the delta (unsigned 64-bit, default 1), `T` updates the TTL on success, `t` returns the TTL, `c` returns the CAS, `v` returns the new value. Return codes `HD`, `NF`, `NS`, `EX`.

Stats: `incr_hits`, `incr_misses`, `decr_hits`, `decr_misses`.

## Checked

2026-11-04. Confirmed against protocol.txt "Increment/Decrement", "Meta Arithmetic" and the general statistics table. Removed: the add-then-incr initialisation recipe (not on the page).

Method: documentation only; no commands were run.
