---
id: computing-software.database-administration.valkey.sets-and-set-operations
name: sets-and-set-operations
category: computing-software
field: database-administration
product: valkey
tags: [sets, sadd, srem, sismember, sinter, sdiff, sunion, sscan, smembers]
level: intro
status: docs-checked
description: "Valkey sets: SADD, SREM, SISMEMBER, SCARD, SINTER, SUNION, SDIFF, SPOP, SRANDMEMBER, order of SDIFF arguments, SMEMBERS cost and SSCAN."
sources:
  - https://valkey.io/topics/sets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Set is an unordered collection of unique strings. Uses: tracking uniques (IP addresses visiting a blog post), representing relations (users with a role), and set algebra. Maximum size is 2^32 - 1 members.

Commands:
- `SADD key member ...` adds; an existing member is ignored, and the reply counts members actually added.
- `SREM` removes one or more members.
- `SISMEMBER` tests membership; `SMISMEMBER` tests several members in one call.
- `SCARD` returns cardinality.
- `SINTER` returns members common to all given sets; `SUNION` and `SDIFF` give union and difference.
- `SPOP` removes and returns a random member; `SRANDMEMBER` returns one without removing.
- `SMEMBERS` returns everything.

Page example: put bikes in `bikes:racing:france` and `bikes:racing:usa`, check `SISMEMBER bikes:racing:usa bike:1`, run `SINTER` to find bikes in both races, `SCARD` to count France entrants (3), and `SDIFF bikes:racing:france bikes:racing:usa` for France-only bikes.

Order matters for `SDIFF`: the difference is not commutative, and it returns an empty array when nothing remains. Sets give no ordering guarantee, so replies may come in any order.

Performance: add, remove and membership are O(1). `SMEMBERS` is O(n) and returns the whole set in one reply, risky for sets of hundreds of thousands of members; use `SSCAN` to iterate in batches.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/sets/ (page text read in full): SADD/SREM/SISMEMBER/SINTER/SCARD, example values (SCARD 3, SDIFF), SUNION, SPOP, SRANDMEMBER, SDIFF order and empty array, 2^32 - 1 limit, SMEMBERS O(n) and SSCAN.

Removed or changed: The unsupported claim that SISMEMBER takes multiple items; the page shows SMISMEMBER for that.

Method: documentation only; no commands were run.
