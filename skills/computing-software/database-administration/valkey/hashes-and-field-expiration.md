---
id: computing-software.database-administration.valkey.hashes-and-field-expiration
name: hashes-and-field-expiration
category: computing-software
field: database-administration
product: valkey
tags: [hashes, hset, hincrby, hexpire, hsetex, hgetex, field-expiration]
level: practitioner
status: docs-checked
description: "Valkey hashes: HSET, HGET, HMGET, HINCRBY, plus Valkey 9.0 per-field TTL with HEXPIRE, HSETEX, HGETEX, HTTL, HPERSIST and the expiry caveats."
sources:
  - https://valkey.io/topics/hashes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hashes are field-value records, good for objects and grouped counters. Field count is limited only by memory (hard cap 2^32 - 1 pairs). Small hashes use a compact encoding that is very memory efficient.

Core commands: `HSET key f v [f v ...]` (multiple fields), `HGET`, `HMGET` (nil for missing fields), `HINCRBY key field n` (negative allowed). Example: `HINCRBY bike:1:stats rides 1`, then `HMGET bike:1:stats owners crashes`. Most commands are O(1); `HKEYS`, `HVALS`, `HGETALL` are O(n).

Field expiration (new in 9.0): a field with a TTL is deleted automatically, and meanwhile every hash command treats an expired field as nonexistent.
- Set: `HEXPIRE`, `HPEXPIRE`, `HEXPIREAT`, `HPEXPIREAT`; remove the TTL with `HPERSIST`.
- Query: `HEXPIRETIME`, `HTTL`, `HPTTL`.
- `HSETEX` sets fields and TTLs together and supports `KEEPTTL`; `HGETEX` reads fields while changing their TTL.
- Plain `HSET` and `HMSET` overwrite a field and clear its TTL.

Caveats: deletion happens in a periodic job, so logically expired fields still use memory and may be counted by `HLEN`. In a big hash mostly made of expired volatile fields, `HRANDFIELD` may not find a live field and can return an empty reply.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/hashes/ (page text read in full): Field-value records, 2^32 - 1 pairs, HSET/HGET/HMGET/HINCRBY with negative increment, compact small-hash encoding, O(1) versus O(n) HKEYS/HVALS/HGETALL, 9.0 field expiration, periodic deletion, HLEN and HRANDFIELD caveats, HSETEX KEEPTTL, HGETEX, HSET/HMSET clearing TTL, HPERSIST (also the notifications page). Note: the hashes page carries an 'under review' banner.

Removed or changed: HPEXPIRETIME, which the page does not list (it names HEXPIRETIME twice).

Method: documentation only; no commands were run.
