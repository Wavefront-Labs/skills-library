---
id: computing-software.database-administration.memcached.stampede-protection-win-flags
name: stampede-protection-win-flags
category: computing-software
field: database-administration
product: memcached
tags: [stampede, dogpile, vivify, win-flag, recache]
level: advanced
status: docs-checked
description: "Prevent cache stampedes atomically with mg N (vivify on miss) and the W win and Z already-won response flags."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Old way: racing clients use `add` after a miss. Meta way, one round trip:

```
mg foo f c v N30
VA 0 f0 c2 W        <- you won: recache it
```
`N30` creates an empty stub item with TTL 30 on a miss. The first client sees `W` (it may now compute and write the value, optionally using CAS `ms foo 3 C2`). Other clients asking meanwhile see `Z`: someone else is recaching; use stale data if present, wait and retry, or take another action.

```
mg foo f c v N30
VA 0 f0 c2 Z
```
Choose N's TTL as the time you allow for recomputation; a stub that is never filled expires on its own.

Related: `R<token>` early recache, `md I` stale serving. The classic non-meta variant is the loose add lock (see loose-lock skill).

Check: two telnet sessions, run the same mg twice; only one gets `W`.

## Checked

Confirmed 2026-11-09: `mg foo f c v N30` vivifies on a miss with TTL 30 and returns `W` to the first client; later clients see `Z`; the client may write back using the CAS; this replaces the older racing `add` approach; `N`, `R`, `W`, `Z` flag definitions (Meta protocol page, Atomic Stampeding Herd Handling; protocol.txt). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Meta protocol page and memcached doc/protocol.txt
