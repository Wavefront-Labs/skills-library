---
id: computing-software.database-administration.memcached.meta-get-flags
name: meta-get-flags
category: computing-software
field: database-administration
product: memcached
tags: [mg, meta-get, flags, ttl, cas]
level: practitioner
status: docs-checked
description: "Reference for mg flags: v value, f client flags, c CAS, t TTL, s size, k key, h/l usage, T touch, u no LRU bump, q quiet, O opaque."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`mg <key> <flags>*` takes a single key. A miss returns `EN`; a hit without `v` returns `HD <flags>`; with `v` it returns `VA <size> <flags>` plus the data block.

Flags that return data: `b` (key is base64 encoded binary), `c` CAS, `f` client flags, `h` hit before (0 or 1), `k` key, `l` seconds since last access, `s` size, `t` TTL remaining (-1 for unlimited), `O<token>` opaque, `q` noreply semantics (suppresses `EN`), `v` the value.
Flags that change behaviour: `u` do not bump the item in the LRU (also avoids marking it hit or updating last access); `T<ttl>` update TTL; `N<ttl>` vivify on miss; `R<token>` win for recache if the remaining TTL is below the token; `E<cas>` use as new CAS value if the item is modified; `C<cas>` check CAS and do not send the value if it matches.

`h` and `l` return the "hit before" and "last access" values from before the command was processed (otherwise `h` would always be 1 and `l` 0).

Replacing classic commands (Meta page):
- get: `mg foo f v`; gets: `mg foo f c v`
- touch: `mg foo T30`; gat: `mg foo f v T90`

Response extras: `W` (client has won the recache), `X` (item is stale), `Z` (another client already received the win flag).

Conditional fetch: with `v` and `C500`, the response is `HD` if the CAS matches and `VA <size>` with the value if it does not, so the value is fetched only if changed. Other flags such as `T` still apply regardless of the CAS match.

## Checked

2026-11-04. Confirmed against protocol.txt (Meta Get) and the Meta page (Replacing GET/GETS/TOUCH/GAT/GATS). Fixed: the `h`/`l` "unless combined with u" qualifier, which misread the page.

Method: documentation only; no commands were run.
