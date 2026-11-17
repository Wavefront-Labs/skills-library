---
id: computing-software.database-administration.memcached.cas-override-versioning
name: cas-override-versioning
category: computing-software
field: database-administration
product: memcached
tags: [cas-override, e-flag, versioning, consistency, multi-pool]
level: advanced
status: docs-checked
description: "Supply your own CAS values with the E flag (1.6.27+) to version cache data by row version, clock or HLC."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

After version 1.6.27 the meta protocol accepts `E<token>` during mutation operations to set the item's CAS instead of the globally incrementing internal counter. The CAS is an 8-byte unsigned value.

```
ms foo 2 E73        -> HD
mg foo c v          -> VA 2 c73
ms foo 2 C72 E73    -> EX   (the second writer fails: the version is already 73)
```
Any command that can generate a new CAS id also accepts E, for example delete with invalidate (`md foo I E74`) and `ma`.

Anything that fits in an 8-byte incrementing number can be used: versions, clocks, HLCs, so long as the next number is higher than the previous one.

Multiple pools (the page says this is not strict): write the leader pool with `ms foo 2 C50 E51`, then issue blind sets with `E51` to the other pools. If all is well all copies have the same CAS as pool A, which helps verify whether data is consistent; if pool A loses the data, you can decide on quorum or highest ID to repair from the others. Fully guaranteeing consistency across pools is difficult if not impossible.

Stronger variant: pick a leader pool, `md foo I E74` invalidates the key and prepares it for the new version, then `mg foo c v` returns the `X` (stale) and `W` (won) flags, giving that client the exclusive right to update the value across pools. If asynchronous updates to the other pools arrive out of order, the highest CAS value should eventually succeed because older ones fail. Failure case from the page: the leader fails after you win and update it but before the others are updated; depending on how leaders are elected, data can end up inconsistent.

## Checked

2026-11-04. Confirmed against the Meta Text Protocol page ("Data consistency with CAS overrides") and protocol.txt (E flag on mg/ms/md/ma). Reworded: equal CAS across pools "implies" consistency (the page says it only helps verify).

Method: documentation only; no commands were run.
