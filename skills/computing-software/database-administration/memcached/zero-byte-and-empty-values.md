---
id: computing-software.database-administration.memcached.zero-byte-and-empty-values
name: zero-byte-and-empty-values
category: computing-software
field: database-administration
product: memcached
tags: [empty-values, zero-byte, get-semantics, advisory-flags, client-bugs]
level: intro
status: docs-checked
description: "Avoid truthiness checks on cached values: 0, false and empty are valid data, and empty keys make cheap flags and locks."
sources:
  - https://docs.memcached.org/userguide/usecases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Don't write:
```
if (data = get('helloworld')) { ... }
```
A cached value of 0, false or empty string is valid data, and falsy in many languages, so a hit looks like a miss.

Use the client's miss indicator (null/undefined, or key presence) instead.

Empty values are useful: advisory locks and status flags often need only key existence, so you can store zero bytes. `ms foo 0` stores an empty value; `mg foo` returns `HD` for existence without sending data.

Related: a recached "not set" flag keeps negative lookups from distorting the hit rate (see measure-hit-rate).

Verify: `set k 0 0 0` then `get k` returns `VALUE k 0 0` with an empty data line.

## Checked

Confirmed 2026-11-09: values of 0, false or empty are valid data, empty keys suit advisory locks and status flags (Use Cases page, Zero byte values); a recached "not set" flag keeps the hit rate accurate (Maintenance page); bytes may be zero and `mg` with no flags returns `HD` (protocol.txt, Meta protocol page). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Use Cases, Maintenance and Meta protocol pages and memcached doc/protocol.txt
