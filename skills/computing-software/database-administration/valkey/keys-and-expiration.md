---
id: computing-software.database-administration.valkey.keys-and-expiration
name: keys-and-expiration
category: computing-software
field: database-administration
product: valkey
tags: [keyspace, keys, expire, ttl, persist, scan, glob-patterns]
level: practitioner
status: docs-checked
description: "Valkey keyspace basics: key naming rules, 512 MB key limit, EXISTS, DEL, TYPE, expiration with EXPIRE and SET EX, SCAN versus KEYS and glob patterns."
sources:
  - https://valkey.io/topics/keyspace/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keys are binary safe: any byte sequence works, including an empty string. Maximum key size is 512 MB, but very long keys (say 1024 bytes) cost memory and slow lookups through extra comparisons; hash a large value (for example SHA1) and use the digest. Too-short keys hurt readability; prefer a schema such as `user:1000:followers`, with dots or dashes for multi-word fields (`comment:4321:reply.to`).

Type-agnostic commands: `EXISTS` and `DEL` return 1 or 0; `TYPE` returns the type name or `none`.

Expiration: any key can get a TTL, set in seconds or milliseconds with resolution always 1 ms. Expiry times are replicated and persisted as absolute dates, so time effectively passes while the server is stopped.
```
SET key some-value
EXPIRE key 5            -> 1
SET key 100 EX 10
TTL key                 -> 9
```
`PEXPIRE` and `PTTL` use milliseconds; `PERSIST` removes the TTL; `EXPIRE` can replace an existing one.

Iteration: `SCAN` returns small batches and is safe in production, but only gives limited guarantees because the keyspace can change mid-iteration. `KEYS` blocks the server until done and should be reserved for debugging or special operations such as relayout, never application code.

Glob patterns: `h?llo`, `h*llo`, `h[ae]llo`, `h[^e]llo`, `h[a-b]llo`; escape literals with a backslash.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/keyspace/ (page text read in full): Binary-safe keys, 512 MB maximum, 1024-byte key and SHA1 advice, schema advice, EXISTS/DEL/TYPE results, seconds or milliseconds with 1 ms resolution, absolute expiry persisted, EXPIRE/SET EX/TTL example, PEXPIRE/PTTL/PERSIST, SCAN versus KEYS, glob patterns.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
