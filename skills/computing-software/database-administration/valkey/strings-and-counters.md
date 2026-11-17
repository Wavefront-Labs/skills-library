---
id: computing-software.database-administration.valkey.strings-and-counters
name: strings-and-counters
category: computing-software
field: database-administration
product: valkey
tags: [strings, set, get, incr, incrby, mset, mget, counters, setnx]
level: intro
status: docs-checked
description: "Valkey strings: SET options, GET, MSET/MGET, GETSET, SETNX, atomic INCR, INCRBY, INCRBYFLOAT, 512 MB limit and O(n) range commands."
sources:
  - https://valkey.io/topics/strings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A String is a byte sequence (text, serialised objects, JPEG data) up to 512 MB by default. Typical uses: caching pages or HTML fragments, counters, bitwise work.

`SET key value` is plain assignment: it overwrites any existing value, even of a different type. Options turn it conditional: fail if the key exists (`NX`) or succeed only if it exists (`XX`), returning `(nil)` when the condition fails. `SETNX` stores only if absent, which is useful for locks. `GET` reads one value; `MSET` and `MGET` set or fetch many keys in one command to cut round trips (`MGET` returns an array).

`GETSET` sets a new value and returns the old one. The page example: a site does `INCR` per visit; once an hour `GETSET` the counter to "0" and read the previous total without losing an increment.

Counters: `INCR` parses the string as an integer, adds one and stores it. Siblings: `INCRBY` (negative to decrement), `DECR`, `DECRBY`, and `INCRBYFLOAT` for floating point. They are atomic: with two clients incrementing a key holding 10, the final value is always 12, because read-modify-write cannot interleave with another command.

Bitwise operations are covered by the bitmaps page.

Performance: most operations are O(1), but `SUBSTR`, `GETRANGE` and `SETRANGE` can be O(n) and hurt on large strings. For structured data serialised into a string, consider a hash instead.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/strings/ (page text read in full): 512 MB limit, SET NX/XX, SETNX, GETSET hourly-counter example, MSET/MGET, INCR parsing and atomicity (final value 12), INCRBY/DECR/DECRBY/INCRBYFLOAT, O(n) SUBSTR/GETRANGE/SETRANGE, hash alternative.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
