---
id: computing-software.database-administration.memcached.loose-lock-with-add
name: loose-lock-with-add
category: computing-software
field: database-administration
product: memcached
tags: [add, loose-lock, stampede, advisory-lock, stampeding-herd]
level: advanced
status: docs-checked
description: "Reduce parallel recache work with an add-based advisory lock and know when it is unsafe."
sources:
  - https://docs.memcached.org/userguide/usecases/
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The docs do not recommend this for any serious locking situation, but for a popular, hard-to-recreate item you can use `add` to create an advisory "loose lock" so dozens of processes do not all hit the database to refill the cache:

```
key  = "expensive_frontpage_item"
item = get(key)
if (!item):
    # give us 60 seconds to recache the item
    if add(key . "_lock", 60):
        item = fetch_expensive_thing_from_database
        add(key, item, 86400)
        delete(key . "_lock")
    else:
        # lost the race: short sleep then re-fetch, try a few times then
        # slow-fetch, show a page without the content, show less expensive
        # content, or throw an error
return item
```
Worst case you operate without the lock at all; best case you reduce parallel queries without adding infrastructure.

Use at your own risk: `add` can fail because the key already exists or because the remote server was down. If your client cannot tell the difference you must decide how hard to try before running the query anyway or throwing an error.

Alternatives named on the page: a third-party outside mutex (for example MySQL `GET_LOCK()` / `RELEASE_LOCK()`), scaling (soft) expiration (see the soft-expiration-recache skill), a job server such as Gearman that coalesces identical jobs; the Meta page replaces the add race with the `N` flag and the `W`/`Z` response flags (see the stampede-protection-win-flags skill).

## Checked

2026-11-04. Confirmed against the Use Cases page (Loose central locking, Avoiding stampeding herd) and the Meta page (Atomic Stampeding Herd Handling). Removed: nothing factual; wording aligned to the page.

Method: documentation only; no commands were run.
