---
id: computing-software.database-administration.memcached.cas-optimistic-update
name: cas-optimistic-update
category: computing-software
field: database-administration
product: memcached
tags: [cas, gets, check-and-set, optimistic-locking, exists]
level: practitioner
status: docs-checked
description: "Use gets plus cas for lock-free read-modify-write and interpret STORED, EXISTS and NOT_FOUND."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

1. Read with `gets key` (or `gat`/`gats`): the reply `VALUE <key> <flags> <bytes> <cas unique>` carries a 64-bit unique.
2. Write with `cas <key> <flags> <exptime> <bytes> <cas unique>`.

Replies: `STORED` if nobody changed it; `EXISTS` if modified since your fetch (re-read and retry); `NOT_FOUND` if it vanished.

Stats: `cas_misses`, `cas_hits`, `cas_badval` (key found but value mismatch).

CAS is on by default (`cas_enabled yes` in `stats settings`);.

Meta form: `mg key c v` returns `c<token>`; `ms key <len> C<token>` stores only on match; the CAS flag also works on `md` and `ma`. After a successful change a new CAS is generated; request it with `c` on `ms`.

## Checked

2026-11-04. Confirmed against protocol.txt (gets, cas, STORED/EXISTS/NOT_FOUND, cas unique, cas_* stats, cas_enabled, meta c and C flags) and the meta protocol page. Removed: the 8 extra header bytes claim and the generic retry tip.

Method: documentation only; no commands were run.
