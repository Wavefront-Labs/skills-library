---
id: computing-software.database-administration.memcached.meta-delete-and-arithmetic
name: meta-delete-and-arithmetic
category: computing-software
field: database-administration
product: memcached
tags: [md, ma, meta-delete, tombstone, invalidate]
level: practitioner
status: docs-checked
description: "Meta delete options (C, I, T, x, q) and ma arithmetic; use md I to mark items stale instead of removing them."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`md <key> <flags>*` replies `HD` (deleted), `NF` (not found) or `EX` (supplied CAS does not match).
- `C<cas>`: delete or mark stale only if the CAS matches.
- `I`: invalidate; instead of removing the item, give it a new CAS and mark it stale. A later `mg` gets the `X` flag (and `W` for the client that wins the recache).
- `T<ttl>`: only with `I`; updates the TTL, limiting how long the item lives while stale and waiting to be recached.
- `x`: removes the item value but leaves the item (replaced atomically by an empty value); combined with `I` this leaves effectively a tombstone of the previous value.
- Also `E<cas>`, `k`, `O<token>`, `q`, `b`.

`ma <key> <flags>*` (see the atomic-counters-incr-decr skill): `N<ttl>` auto-create on miss, `J<initial>`, `D<delta>`, `T<ttl>`, `M` mode (`I` or `+` increment, `D` or `-` decrement), `v` return the new value, `t`, `c`, `k`, `q`, `C`, `E`. Replies `HD`, `NF`, `NS`, `EX`; with `v`, `VA <size>` followed by the number.

Examples: `md foo I T30` -> `HD` (marks stale for up to 30 seconds); `ma hits N0 J0 D1 v`.

Values are unsigned 64-bit: decrementing reaches 0 rather than underflowing, incrementing can overflow.

## Checked

2026-11-04. Confirmed against protocol.txt (Meta Delete, Meta Arithmetic) and the Meta page (Serve Stale example). Removed: nothing factual; wording aligned to the page.

Method: documentation only; no commands were run.
