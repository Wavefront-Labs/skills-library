---
id: computing-software.database-administration.valkey.bitmaps-setbit-bitcount
name: bitmaps-setbit-bitcount
category: computing-software
field: database-administration
product: valkey
tags: [bitmaps, setbit, getbit, bitop, bitcount, bitpos]
level: intro
status: docs-checked
description: "Valkey bitmaps: SETBIT, GETBIT, BITOP, BITCOUNT, BITPOS on strings as bit vectors, 512 MB limit, space savings and key-splitting strategy."
sources:
  - https://valkey.io/topics/bitmaps/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bitmaps are not a data type: they are bit-oriented commands on the String type, treated as a bit vector. Strings are binary safe with a 512 MB maximum, so a single key addresses up to 2^32 bits. Use cases: sets over integers 0..N, permission flags, per-user yes/no facts. Tracking one bit for 4 billion users takes about 512 MB.

Single-bit, O(1):
- `SETBIT key offset 0|1` grows the string automatically if the offset is beyond its length.
- `GETBIT key offset`; bits beyond the string end read as 0.

Group operations:
- `BITOP` applies AND, OR, XOR or NOT across strings, O(n) in the longest string.
- `BITCOUNT` counts set bits (population count).
- `BITPOS` finds the first bit equal to 0 or 1.
`BITCOUNT` and `BITPOS` accept byte ranges so they need not scan the whole string.

Example, hourly sensor check-ins for 1000 riders:
```
SETBIT pings:2024-01-01-00:00 123 1
GETBIT pings:2024-01-01-00:00 123    -> 1
GETBIT pings:2024-01-01-00:00 456    -> 0
BITCOUNT pings:2024-01-01-00:00
```
Daily-visit streaks: bit index = (unix time minus launch time) divided by 86400; `BITCOUNT` gives days visited, and `BITPOS` calls or client-side analysis give the longest streak.

Avoid huge keys: shard a bitmap by storing M bits per key, using key suffix `bit / M` and in-key offset `bit MOD M`.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/bitmaps/ (page text read in full): Bit operations on Strings, 512 MB and 2^32 bits, use cases, 4 billion users in 512 MB, SETBIT growth, GETBIT out-of-range zero, BITOP AND/OR/XOR/NOT, BITCOUNT, BITPOS, byte ranges, cyclist example, streak method, bit-number/M and MOD M splitting, O(1) and O(n).

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
