---
id: computing-software.database-administration.redis.strings-and-atomic-counters
name: strings-and-atomic-counters
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, strings, set, incr, counters, getex, idempotency, ttl]
level: practitioner
status: docs-checked
description: "Use Redis string commands correctly: SET with EX/NX/XX/GET/KEEPTTL, atomic INCR/INCRBY counters with expiry, limits and encodings, and idempotency keys."
sources:
  - https://redis.io/docs/latest/commands/set/
  - https://redis.io/docs/latest/commands/incr/
  - https://redis.io/docs/latest/commands/expire/
  - https://redis.io/docs/latest/develop/data-types/strings/
  - https://redis.io/docs/latest/commands/object-encoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings and atomic counters

**Goal:** the right string commands for caches, counters and idempotency keys, without race conditions.

## Set with options (one round trip, atomic)
```text
SET session:abc '{"uid":42}' EX 1800          # value + TTL
SET lock:job:7 worker-3 NX PX 30000           # only if absent, 30 s expiry
SET config:v2 data XX KEEPTTL                 # only if exists, keep the existing TTL (KEEPTTL 6.0+)
SET counter 0 GET                             # returns the old value (6.2+); replaces GETSET
```
Grammar: `SET key value [NX | XX | IFEQ v | IFNE v | IFDEQ d | IFDNE d] [GET] [EX s | PX ms | EXAT ts | PXAT ms-ts | KEEPTTL]`
(`IF*` conditions need 8.4; `EXAT`/`PXAT` and `GET` need 6.2). A plain `SET` discards any previous TTL.
`SETNX` + `EXPIRE` as two commands is racy (a crash between them leaves a key without TTL); use `SET ... NX EX`.
The SET page notes that `SETNX`, `SETEX`, `PSETEX` and `GETSET` may be deprecated in future versions.

## Counters
```text
INCR page:views:2026-10-18         # creates the key at 0 if missing, returns the new value
INCRBY quota:user:42 5
DECRBY stock:sku:9 1
INCRBYFLOAT price:avg 0.25         # stored as a string, beware float rounding
```
Atomic on the server: safe under concurrency without WATCH. `INCR` is limited to 64-bit signed integers and returns an
error if the value is not an integer string. Redis stores integer-valued strings in an integer representation with no extra overhead.

Daily counter with expiry:
```text
MULTI
INCR hits:2026-10-18
EXPIRE hits:2026-10-18 172800 NX     # 7.0+: set the TTL only if none exists
EXEC
```
`INCR`, `LPUSH` and `HSET` leave an existing TTL untouched; only commands that delete or overwrite the key (`DEL`, `SET`, `GETSET`, `*STORE`) clear it.

## Other useful string commands
- `MGET`/`MSET` batch reads/writes (in a cluster, all keys must be in one slot, e.g. via a hash tag).
- `GETEX key EX 60` (6.2+) reads and refreshes the TTL; `GETDEL` (6.2+) reads and deletes.
- `APPEND`, `GETRANGE`, `SETRANGE`, `STRLEN` for partial access. `GETRANGE`, `SETRANGE` and `SUBSTR` can be O(n), which matters on large strings.
- `SET` with `NX` returns nil if the key exists, which makes it an idempotency key: `SET idem:<request-id> 1 NX EX 86400`.

## Limits and encoding
- A string can be at most 512 MB by default. Large values make reads, writes and deletes slower (no size threshold is documented, so measure); `UNLINK` frees big values off-thread.
- `OBJECT ENCODING key` returns `int` (integers in the 64-bit signed range), `embstr` (strings up to 44 bytes) or `raw`.
- Many tiny keys have per-key overhead; grouping small fields in a hash can be much cheaper (see the hashes skill).

## Verify
`redis-cli --bigkeys` finds oversized strings; `TTL key` confirms expiries are set (`-1` means no TTL, a leak risk).

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): SET, INCR, EXPIRE, strings data type page,
OBJECT ENCODING. Confirmed: SET grammar and since-versions (NX/XX 2.6.12, GET 6.2.0, EXAT/PXAT 6.2.0, KEEPTTL 6.0.0, IF*
8.4.0), TTL discard behaviour, `EXPIRE ... NX` since 7.0.0, `INCR` 64-bit signed limit and creation at 0, TTL
retention rules, 512 MB limit, O(n) warning for GETRANGE/SETRANGE/SUBSTR, `embstr` limit 44 bytes, SET deprecation note.
Also confirmed from the strings page: GETEX and GETDEL exist since 6.2.0. Removed: the "< 100 KB" size advice (no
threshold is documented).
Method: documentation only; no commands were run.
