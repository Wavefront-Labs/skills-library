---
id: computing-software.database-administration.valkey.persistence-rdb-vs-aof
name: persistence-rdb-vs-aof
category: computing-software
field: database-administration
product: valkey
tags: [persistence, rdb, aof, appendonly, appendfsync, snapshot, save, bgsave]
level: practitioner
status: docs-checked
description: "Valkey persistence choices: RDB snapshots (save 60 1000, dump.rdb, fork), AOF with appendonly and appendfsync policies, multi-part AOF, and when to combine."
sources:
  - https://valkey.io/topics/persistence/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Four options: RDB point-in-time snapshots, AOF (log of every write in protocol format, replayed at startup), none (cache use), or both.

RDB: compact single file, ideal for backups and disaster recovery, restarts faster than AOF, and the parent only forks (the child does disk I/O), maximising performance. Weakness: writes since the last snapshot are lost on a crash. Snapshots are on by default to `dump.rdb`; `save 60 1000` dumps every 60 s if at least 1000 keys changed; `SAVE`/`BGSAVE` run manually. Disable with `save ""` (or `--save ""`). Mechanism: fork, child writes a temporary RDB, then replaces the old file (copy-on-write).

AOF: enable with `appendonly yes`. `appendfsync` policies:
- `always`: fsync after each batch of commands (one write, one fsync before replies); very safe, very slow, supports group commit.
- `everysec`: default; fsync each second via a background thread, so at most one second of loss.
- `no`: leave it to the OS (Linux typically flushes every 30 s).
AOF is append-only, so power loss does not corrupt it; files are usually bigger than RDB and can be slower. It is multi-part: at most one base file (RDB or AOF format) plus incremental files in a directory, tracked by a manifest.

Guidance: use both for safety comparable to PostgreSQL; RDB alone if a few minutes of loss is acceptable; AOF alone is discouraged because RDB gives backups, faster restarts and protection from AOF bugs. With both enabled, restart loads the AOF, as it is most complete.

## Checked
2026-11-03. Confirmed against the Valkey Persistence page (valkey.io/topics/persistence/): the four options, RDB advantages and weakness, default `dump.rdb`, `save 60 1000`, `save ""` and `--save ""`, fork and temporary-file mechanism, `appendonly yes`, the three `appendfsync` policies (Linux flush about every 30 s with `no`), multi-part AOF structure, the recommendation to combine both, and the AOF-first restart rule. Nothing removed.
Method: documentation only; no commands were run.
