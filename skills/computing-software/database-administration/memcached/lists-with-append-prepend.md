---
id: computing-software.database-administration.memcached.lists-with-append-prepend
name: lists-with-append-prepend
category: computing-software
field: database-administration
product: memcached
tags: [append, prepend, lists, blacklist, item-size]
level: advanced
status: docs-checked
description: "Maintain lists in a single key with atomic append and prepend, using a zero marker for removals; mind the 1 MB limit."
sources:
  - https://docs.memcached.org/userguide/usecases/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Storing lists means either one item with a serialized array, or manipulating a collection by adding and removing items without touching the whole set. Mind memcached's 1 megabyte item size limit. For a list of ids you can use `append`/`prepend` for atomic updates instead of a CAS update or deleting the cache and reloading from the database.

Add an id: issue `append` with a binary packed string representing the id. Like incr/decr, append fails if the cache list does not already exist. So: append; if it fails, load from the database and `add`; if that fails, decide how much you care about ensuring the item got in and do more work.

Removal without rewriting: when initializing the list, the first entry can be a "zero marker", a whole four or eight byte value (depending on how big your ids are) containing nothing but zeros. When loading, the first items you read are "blacklist" items; once you hit the zero value, the rest are items that should exist, and you check each against the blacklist before displaying it. Add new ids at the end and prepend removed ids to the front.

If the cache is blown and reloaded, the rebuilt entry does not contain the blacklisted items, so the entry is cleaned. The guide notes obvious limitations based on cache size; for larger collections it points to approaches with ids in ranges stored in separate keys and data in individual keys (mailing-list posts linked there).

Meta alternative (protocol.txt): `ms key <datalen> MA N<ttl>` appends and, with `N`, creates the item on a miss using the append data and the N ttl.

## Checked

2026-11-04. Confirmed against the Use Cases page (Storing sets or lists, Managing lists with append/prepend) and protocol.txt (ms M and N flags). Removed: the closing "Check with get and compare bytes" line.

Method: documentation only; no commands were run.
