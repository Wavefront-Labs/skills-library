---
id: computing-software.database-administration.memcached.meta-set-modes-and-flags
name: meta-set-modes-and-flags
category: computing-software
field: database-administration
product: memcached
tags: [ms, meta-set, mode-switch, append, invalidate]
level: practitioner
status: docs-checked
description: "Store with ms: datalen, flags T F C E I q O b s c k, modes via M (E add, A append, P prepend, R replace, S set) and N autovivify."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`ms <key> <datalen> <flags>*\r\n<data block>\r\n`. Codes: `HD` (stored), `NS` (not stored, not an error), `EX` (exists: CAS mismatch), `NF` (not found: CAS semantics on a missing item).

Flags:
- `T<ttl>`; `F<token>` sets client flags (32-bit unsigned; 0 if not supplied).
- `C<cas>` compare CAS; `E<cas>` use as the new CAS; `I` invalidate: with `C`, a CAS lower than the current one may be accepted but the item is marked stale (mg then returns `X`).
- `M<mode>`: `E` add (LRU bump and return NS if the item exists), `A` append, `P` prepend, `R` replace, `S` set (the default).
- `N<ttl>`: in append mode, autovivify on miss with the supplied TTL (used instead of T).
- `c` return CAS on success, `s` return the size of the stored item (for example the new size on append), `k` key, `O<token>`, `q` hide `HD`, `b` base64 key.

Examples:
```
ms foo 2 T60 F5\r\nhi
ms foo 3 MA N60\r\nabc     append, create if missing
ms foo 3 C999\r\nnew       store only if CAS is 999
```
Append and prepend modes respect a supplied CAS. The classic `cas` command is replaced by the `C` flag.

`c` returns 0 on error, but clients must not depend on the value being zero.

## Checked

2026-11-04. Confirmed against protocol.txt (Meta Set). Removed: nothing factual; wording aligned to the page.

Method: documentation only; no commands were run.
