---
id: computing-software.database-administration.memcached.serve-stale-with-md-invalidate
name: serve-stale-with-md-invalidate
category: computing-software
field: database-administration
product: memcached
tags: [stale-while-revalidate, serve-stale, invalidate, x-flag, md]
level: advanced
status: docs-checked
description: "Implement stale-while-revalidate: md I marks an item stale, mg returns X and W, and ms I keeps it stale while you update."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Mark stale instead of deleting:
```
md foo I T30         -> HD   (stale data lives at most 30 s; CAS changes)
mg foo t c v         -> VA 4 t29 c777 W X
data
```
`X` means stale, `W` means this client alone owns the recache. The app decides whether stale data is safe to show.

Another `md` before the recache bumps the CAS (778), so a later `ms ... C777` fails with `EX`. To update but remain stale, use `I` on ms with the older CAS:
```
ms foo 3 T360 C777 I
```
Following `mg` calls still see `X`, with the old TTL and CAS; the CAS you pass must be lower than the real one for this to apply. Once a set with a matching CAS arrives, the data and TTL are fully replaced.

Also `md foo I x` leaves a tombstone (value removed, item kept).

Test with `mg foo t c v` repeatedly and expect W only once, then Z.

## Checked

Confirmed 2026-11-09: `md foo I T30` marks an item stale, changes the CAS and optionally the TTL; `mg` then returns `W` and `X`; a second `md` bumps the CAS so a later `ms` with the old CAS fails; `ms` with `I` and a lower CAS keeps the item stale with the previous TTL and CAS, and a matching CAS set overwrites everything; `x` on `md` removes the value but leaves the item; flag meanings W, X, Z (Meta protocol page and protocol.txt metaget, metaset and metadelete sections). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Meta protocol page and memcached doc/protocol.txt
