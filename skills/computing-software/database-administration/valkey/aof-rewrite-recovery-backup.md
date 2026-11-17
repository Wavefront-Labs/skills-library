---
id: computing-software.database-administration.valkey.aof-rewrite-recovery-backup
name: aof-rewrite-recovery-backup
category: computing-software
field: database-administration
product: valkey
tags: [aof, bgrewriteaof, valkey-check-aof, aof-load-truncated, backup, auto-aof-rewrite-percentage, appenddirname]
level: advanced
status: docs-checked
description: "Valkey AOF operations: BGREWRITEAOF and multi-part rewrite, truncated or corrupt AOF repair with valkey-check-aof, RDB-to-AOF switch, consistent backups."
sources:
  - https://valkey.io/topics/persistence/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rewrite: the AOF grows (100 `INCR`s leave 100 entries for one key), so `BGREWRITEAOF` or automatic triggers write the minimal commands to rebuild the dataset. The parent opens a new incremental file, a child writes a new base file, a temporary manifest is built, then swapped atomically; old files are deleted. A failed rewrite is safe (old base plus all increments remain) and retries back off slower and slower. If an RDB snapshot is running, `BGREWRITEAOF` replies OK and starts afterwards.

Truncated tail: with `aof-load-truncated` enabled (default) the server drops the last malformed command and logs a short-read warning. Older versions need `valkey-check-aof --fix <filename>` after a backup copy. Mid-file corruption aborts startup ("Bad file format"); run `valkey-check-aof` without `--fix` first, inspect the offset, repair by hand if possible, because `--fix` discards everything from the bad point to the end.

RDB to AOF on a live server: back up `dump.rdb`, then `CONFIG SET appendonly yes` (optionally `CONFIG SET save ""`), confirm writes append, and update `valkey.conf` (or `CONFIG REWRITE`) or a restart loses the change. Before restarting, wait until `INFO persistence` shows `aof_rewrite_in_progress` and `aof_rewrite_scheduled` at 0 and `aof_last_bgrewrite_status` ok.

Backups: RDB files can be copied while running (written under a temporary name, renamed atomically). For AOF directories (`appenddirname`): set `auto-aof-rewrite-percentage 0`, check `aof_rewrite_in_progress` is 0, copy or hard-link, then restore the old value; use `CONFIG REWRITE` to survive restarts. Verify transferred backups by size and SHA1.

## Checked
2026-11-03. Confirmed against the Valkey Persistence page (valkey.io/topics/persistence/): log rewriting and multi-part AOF steps, slower retries after failed rewrites, `BGREWRITEAOF` during a snapshot, `aof-load-truncated` and the short-read log, `valkey-check-aof --fix` behaviour, the RDB-to-AOF switch procedure with the `INFO persistence` fields, and the AOF backup procedure with `auto-aof-rewrite-percentage`, hard links and `CONFIG REWRITE`. Nothing removed.
Method: documentation only; no commands were run.
