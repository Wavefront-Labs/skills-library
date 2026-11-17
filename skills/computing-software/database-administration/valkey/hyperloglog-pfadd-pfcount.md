---
id: computing-software.database-administration.valkey.hyperloglog-pfadd-pfcount
name: hyperloglog-pfadd-pfcount
category: computing-software
field: database-administration
product: valkey
tags: [hyperloglog, pfadd, pfcount, pfmerge, cardinality, unique-counts]
level: intro
status: docs-checked
description: "Valkey HyperLogLog: PFADD, PFCOUNT, PFMERGE for approximate unique counts in at most 12 KB with 0.81% standard error."
sources:
  - https://valkey.io/topics/hyperloglogs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HyperLogLog (HLL) estimates set cardinality in constant memory: at most 12 KB (far less when few elements are seen), standard error 0.81%, up to 2^64 members. It is stored as a String, so `GET` serialises one and `SET` restores it.

The API mirrors a Set used for counting (`SADD` plus `SCARD`), but no elements are kept:
- `PFADD key element [element ...]` registers observations; replies 1 in the page example.
- `PFCOUNT key [key ...]` returns the approximate unique count.
- `PFMERGE dest src [src ...]` unions HLLs, so the result estimates uniques across all sources.

Example from the page:
```
PFADD bikes Hyperion Deimos Phoebe Quaoar     -> 1
PFCOUNT bikes                                 -> 4
PFADD commuter_bikes Salacia Mimas Quaoar
PFMERGE all_bikes bikes commuter_bikes        -> OK
PFCOUNT all_bikes                             -> 6
```
Overlapping element `Quaoar` is counted once.

Use cases: unique queries per day in a search form, unique visitors per page, unique plays per song or video. Keep one HLL per page/item per period and add the visitor identifier on every visit. The page notes storing IPs or personal identifiers is illegal in some countries, which an HLL avoids because it stores no elements.

Cost: `PFADD` and `PFCOUNT` are constant time and space; `PFMERGE` is O(n) in the number of sketches.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/hyperloglogs/ (page text read in full): 12 KB, 0.81% standard error, 2^64 members, String encoding with GET/SET, SADD/SCARD analogy, PFADD/PFCOUNT/PFMERGE example values (4 and 6), use cases, personal-identifier note, constant time and O(n) merge.

Removed or changed: The unsupported statement that PFADD returns 1 when the estimate changed (the page only shows 1 in its example).

Method: documentation only; no commands were run.
