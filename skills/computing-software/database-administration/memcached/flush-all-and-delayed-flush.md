---
id: computing-software.database-administration.memcached.flush-all-and-delayed-flush
name: flush-all-and-delayed-flush
category: computing-software
field: database-administration
product: memcached
tags: [flush-all, invalidate, delayed-flush, cmd-flush, delete]
level: practitioner
status: docs-checked
description: "Invalidate a cache with flush_all, understand it does not free memory, and stagger flushes across a pool with a delay."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/serverguide/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`flush_all [delay] [noreply]` always succeeds and replies `OK` (unless `noreply` is given). It causes all items whose update time is earlier than the time the flush was set to execute to be ignored for retrieval. It does not free all the memory taken by existing items; that happens gradually as new items are stored. Items stored again under the same key after the flush has invalidated the old ones are returned normally.

Staggering: the delay option lets you reset a pool of servers at intervals (pass 0 to the first, 10 to the second, 20 to the third, and so on) instead of all at once, which could spike database load as every client recreates content.

Monitoring: every flush_all increments `cmd_flush` (Maintenance page: sound the alarms if it moves unexpectedly, since debug code or callbacks can leave scripts flushing the whole cache); `get_flushed` counts requested items that had been flushed via flush_all.

Single keys: `delete <key>` returns `DELETED` or `NOT_FOUND`; meta `md key` returns `HD` or `NF`. To invalidate only a subset, the Use Cases docs describe emulating namespaces with versioned key prefixes.

## Checked

2026-11-04. Confirmed against protocol.txt ("Other commands" flush_all, delete, md, get_flushed) and the Maintenance page (cmd_flush). Removed: the unqualified "prefer namespace versioning" advice.

Method: documentation only; no commands were run.
