---
id: computing-software.database-administration.valkey.bitfields
name: bitfields
category: computing-software
field: database-administration
product: valkey
tags: [bitfield, bitfield-ro, counters, integers, incrby]
level: intro
status: docs-checked
description: "Valkey BITFIELD: atomic get, set and incrby on arbitrary-width integers (u1 to i63) inside a string, plus BITFIELD_RO."
sources:
  - https://valkey.io/topics/bitfields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bitfields store integers of arbitrary bit width, from unsigned 1-bit to signed 63-bit, inside an ordinary binary-encoded String. Reads, writes and increments are atomic, which makes them suited to packed counters.

Commands: `BITFIELD key ...` performs one or more sub-operations (`SET`, `GET`, `INCRBY`) atomically in a single call, and `BITFIELD_RO` is the read-only variant.

The page example uses type `u32` with offsets `#0` and `#1` for its two counters; look up the BITFIELD command page for the full type and offset syntax.

Example from the page, two 32-bit counters per bike:
```
BITFIELD bike:1:stats SET u32 #0 1000
BITFIELD bike:1:stats INCRBY u32 #0 -50 INCRBY u32 #1 1
BITFIELD bike:1:stats GET u32 #0 GET u32 #1
```
`SET` replied 0 in the example; the `INCRBY` call returns `950` and `1` as an array, one reply per sub-operation. Negative increments are allowed. Later calls on the page raise price by 500 and owners by 1, giving `1450` and `2`.

Cost: `BITFIELD` is O(n) where n is the number of counters accessed in the call. Values are stored in a binary-encoded String.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/bitfields/ (page text read in full): Arbitrary widths from unsigned 1-bit to signed 63-bit, binary-encoded Strings, atomic read/write/increment, BITFIELD and BITFIELD_RO, the bike:1:stats example outputs (0, 950 and 1, 1450 and 2), O(n).

Removed or changed: The claim that #n means the n-th slot of that width, the 'signedness plus width' type grammar, the SET-returns-old-value rule and the claim that the key can be used with bitmap commands; the page does not state them.

Method: documentation only; no commands were run.
