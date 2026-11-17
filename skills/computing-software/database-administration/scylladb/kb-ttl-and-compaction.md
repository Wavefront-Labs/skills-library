---
id: computing-software.database-administration.scylladb.kb-ttl-and-compaction
name: kb-ttl-and-compaction
category: computing-software
field: database-administration
product: scylladb
tags: [ttl, gc-grace-seconds, tombstones, compaction, twcs]
level: advanced
status: docs-checked
description: "How expired TTL data is removed in ScyllaDB: expired cells become tombstones unless timestamp plus gc_grace_seconds has passed, TTL above gc_grace_seconds, and TWCS."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/ttl-facts.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TTL, gc_grace_seconds and compaction

Applies to per-write CQL TTL; the per-row TTL extension behaves differently.

Facts:
1. When compaction scans an expired cell:
   - If `data timestamp + gc_grace_seconds <= now`, the data is dropped and **no tombstone** is created.
   - Otherwise a tombstone is created whose timestamp equals the original cell timestamp (its `local_deletion_time` shows the expired cell timestamp). That tombstone can be purged only after at least `gc_grace_seconds` from the data write.
2. If TTL is greater than `gc_grace_seconds`, expired data never generates a tombstone: by the time it expires, the grace period has already elapsed.
3. TWCS decides whether an SSTable can be deleted by treating expired data like a tombstone: it compares the max deletion time (write time plus TTL) of overlapping SSTables with the grace period, so whole SSTables can be dropped without rewriting.

Example from the page: with `gc_grace_seconds: 0`, SSTable A (timestamp 1, TTL 2, max deletion time 3) and SSTable B (timestamps 1 to 5, TTL 2, max deletion time 7) over the same token: with now at 6, A is fully expired (3 < 6) and B is not (7 > 6), but compaction does not purge A: A overlaps B in token and timestamp range, so it may hold a tombstone shadowing data in B.

Updates combined with TWCS may keep window-compacted SSTables from being deleted when expected; once the data has expired in all SSTables, the relevant SSTables are deleted at the next compaction.

## Checked

2026-11-04: the compaction rules, the TTL greater than gc_grace_seconds case and the TWCS example confirmed against the ScyllaDB TTL and compaction knowledge-base page. Removed the unsupported operational advice and corrected the example outcome.

Method: documentation only; no commands were run.
