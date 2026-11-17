---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tail-start-position-and-db
name: tail-start-position-and-db
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tail-input, db, read-from-head, offsets, at-least-once]
level: practitioner
status: docs-checked
description: "Decide where the tail input starts reading and keep offsets in a per-input database for restart safety."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/tail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tail start position and database

Where `tail` begins reading a file depends on the database and `read_from_head`.

- **With a `db` file**: the plugin restores the last known offset. If no position exists and `read_from_head` is `false`, it starts at the end of the file.
- **Without a `db`**: `read_from_head: true` reads from the start; `false` (default) starts at the end, the classic `tail -f` behaviour, so only content written after Fluent Bit starts is seen.

`read_from_head` applies to files discovered at startup. `read_newly_discovered_files_from_head` (default `true`) does the same for files discovered after startup.

The database stores `inode=offset`, so give each tail input its own file. It is backed by SQLite3.

```yaml
pipeline:
  inputs:
    - name: tail
      path: /var/log/app/*.log
      db: /var/lib/fluent-bit/app.db
      read_from_head: true
```

Delivery guarantees: on normal operation and graceful shutdown (SIGTERM) offsets are synchronised to the database. After an unexpected shutdown such as a crash, power loss or SIGKILL, Fluent Bit guarantees at-least-once delivery: the stored offset may trail the processed position, so on restart it resumes from the last committed checkpoint and a minimal amount of data may be re-ingested as duplicates.

Related keys: `db.sync` selects the SQLite synchronisation method (default `normal`; `full` has a high I/O cost), `db.journal_mode` defaults to `wal` (not compatible with shared network file systems), and `db.locking: true` speeds database access but stops external tools querying it. `db.compare_filename` (default `false`) makes lookups check both inode and filename instead of the inode alone.

When opening the database with the sqlite3 client while Fluent Bit runs, you may see `Error: database is locked`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs tail input page (raw markdown, read in full).
