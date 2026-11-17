---
id: computing-software.database-administration.redis.json-documents-with-redisjson
name: json-documents-with-redisjson
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-json, json-set, jsonpath, redis-stack, redis-data-types]
level: practitioner
status: docs-checked
description: "Store and update JSON documents in Redis (JSON.SET/JSON.GET with JSONPath, atomic sub-document updates), with memory, indexing and version notes."
sources:
  - https://redis.io/docs/latest/develop/data-types/json/
  - https://redis.io/docs/latest/develop/data-types/json/path/
  - https://redis.io/docs/latest/commands/json.set/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON documents (JSON.SET / JSONPath)

**Goal:** keep a structured document in one key and update nested fields atomically, instead of serialising whole strings or flattening to hashes. JSON is built into Redis 8 (Redis Open Source); on older versions it needs the RedisJSON module (Redis Stack).

## Write and read
```text
JSON.SET user:42 $ '{"name":"Ana","tags":["admin"],"address":{"city":"Perth"},"logins":0}'
JSON.GET user:42 $.address.city                  # ["Perth"]
JSON.GET user:42 $.name $.logins                  # several paths
JSON.MGET user:42 user:43 $.name
```

## Atomic partial updates
```text
JSON.SET user:42 $.address.city '"Fremantle"'
JSON.NUMINCRBY user:42 $.logins 1
JSON.ARRAPPEND user:42 $.tags '"billing"'
JSON.DEL user:42 $.address
JSON.SET user:42 $.email '"a@x.io"' NX           # add only if path missing
```
Each command is atomic on the key; no read-modify-write race.

## JSONPath notes
- `$` syntax (JSONPath) returns arrays of matches; legacy `.` syntax returns single values. Use `$` in new code.
- Filters: `JSON.GET orders:9 '$.items[?(@.qty>2)].sku'`.
- Recursive descent `$..price` retrieves a field from multiple sections of the document at any depth.

## Memory and size
- Documents are stored as binary data in a tree structure. `JSON.DEBUG MEMORY user:42` reports memory use (the docs warn that real usage can be lower because of internal string reuse).
- Nesting is limited to 128 levels of objects or arrays.

## Querying across documents
Create an index with the query engine: `FT.CREATE idx:users ON JSON PREFIX 1 user: SCHEMA $.address.city AS city TAG $.logins AS logins NUMERIC`, then `FT.SEARCH idx:users '@city:{Perth}'`.

## Gotchas
- Cluster: `JSON.MGET` needs all keys in one hash slot; across slots it returns no CROSSSLOT error and the results may be partial.

## Verify
`JSON.TYPE user:42 $` returns the type of the root value and `JSON.GET user:42 $.name` returns `["Ana"]`.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed: JSON is part of Redis Open Source and Redis 8 merges Stack into it; JSON.SET syntax with NX (no matches) and XX; `$` starts JSONPath and returns a top-level array, a legacy path returns a single value; JSON.GET with several paths returns an object; JSON.NUMINCRBY and JSON.ARRAPPEND syntax; JSON.MGET takes one trailing path and needs one slot in cluster; `JSON.DEBUG MEMORY key [path]`; 128-level nesting limit; FT.CREATE ON JSON/PREFIX/SCHEMA grammar. Removed unconfirmed: TYPE returning ReJSON-RL, performance claims for recursive descent, size guidance, third-party dump tool note.
Method: documentation only; no commands were run.
