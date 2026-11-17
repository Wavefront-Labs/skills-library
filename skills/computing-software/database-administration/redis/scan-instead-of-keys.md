---
id: computing-software.database-administration.redis.scan-instead-of-keys
name: scan-instead-of-keys
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, scan, keys, hscan, sscan, zscan, unlink, cursor, blocking-commands, scan-cursor]
level: practitioner
status: docs-checked
description: "Replace Redis KEYS with cursor-based SCAN/HSCAN/SSCAN/ZSCAN, handle duplicates and empty pages, delete by pattern safely, and avoid scans in Cluster hot paths."
sources:
  - https://redis.io/docs/latest/commands/scan/
  - https://redis.io/docs/latest/commands/hscan/
  - https://redis.io/docs/latest/develop/tools/cli/
  - https://redis.io/docs/latest/develop/using-commands/multi-key-operations/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SCAN instead of KEYS

`KEYS pattern` walks the entire keyspace in one call; Redis executes commands on a single thread, so
on millions of keys it blocks every client. Never use it in production code.
Disable it for app users via ACL (`-keys`).

## SCAN
```
SCAN 0 MATCH session:* COUNT 1000 TYPE string
1) "17732"           # next cursor
2) 1) "session:ab12" ...
SCAN 17732 MATCH session:* COUNT 1000
...                  # repeat until the cursor returned is "0"
```
- `COUNT` is a hint of the work to do per call (default 10), not a result count. A call may return zero
  elements with a non-zero cursor: keep iterating until the cursor is 0. When the keyspace or a collection is a
  small encoded structure, one call can return everything.
- `TYPE` (6.0+) filters by type server-side and exists only on the whole-database `SCAN`, not on `HSCAN`/`ZSCAN`.
- Guarantees: an element present for the whole iteration is always returned; elements may be returned
  **more than once**; elements added or removed during the scan may or may not appear.
  Deduplicate client-side, or only apply operations that are safe to repeat.

CLI shortcut: `redis-cli --scan --pattern 'session:*' --count 1000` (add `-i 0.01` to throttle between SCAN calls).

## Collections
`HSCAN key cursor [MATCH pattern] [COUNT count] [NOVALUES]` (`NOVALUES` since 7.4), `SSCAN`, `ZSCAN` iterate big hashes,
sets and sorted sets instead of `HGETALL` / `SMEMBERS` / `ZRANGE 0 -1` on huge keys.

## Bulk delete by pattern
```bash
redis-cli --scan --pattern 'cache:v1:*' --count 1000 | xargs -n 500 redis-cli UNLINK
```
`UNLINK` does the memory reclaiming in a background thread (unlike `DEL`, which blocks). In an open source
Redis Cluster, `SCAN` covers only the shard (node) you are connected to, so run the scan on **each master**, and a
multi-key `UNLINK` must have all keys in one hash slot, so send keys individually or grouped by slot.
Since Redis 8.0, a `MATCH` pattern that begins with a hash tag, such as `{abc}*`, searches only that one slot.

From Lua/functions: do not scan the whole keyspace inside one script (it blocks); drive the loop from the client.

## Better than scanning
If you regularly need "all keys of X", keep an index: a set of member keys
(`SADD idx:sessions session:ab12`) or put related data in one hash. Use key expiry (TTL) for
cache invalidation rather than pattern deletes.

## Verify
`SLOWLOG GET` shows no `KEYS` calls; scanning scripts complete with the cursor reaching 0 and
latency (`redis-cli --latency`) stays flat during the run.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): SCAN, HSCAN, redis-cli reference,
multi-key operations page, cluster specification (pattern slot optimisation, 8.0), ACL page. Confirmed: SCAN syntax,
default COUNT 10, TYPE since 6.0.0 and whole-DB only, guarantees and zero-element pages, `HSCAN ... NOVALUES` since 7.4,
`--scan`/`--pattern`/`--count`/`-i`, per-shard behaviour of SCAN and single-slot UNLINK, `-keys` ACL rule.
Removed: `rename-command` as a way to disable KEYS (not covered in the sources read).
Method: documentation only; no commands were run.
