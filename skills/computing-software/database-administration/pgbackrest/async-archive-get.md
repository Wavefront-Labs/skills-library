---
id: computing-software.database-administration.pgbackrest.async-archive-get
name: async-archive-get
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, archive-async, archive-get, queue, standby]
level: advanced
status: docs-checked
description: "Maintain a local WAL queue for archive-get to speed recovery from high-latency repositories."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: feed recovery faster.

Asynchronous archive-get keeps a queue of WAL in the spool path. If a segment is missing from the queue, it is fetched together with enough consecutive WAL to fill the queue. The queue maximum is `archive-get-queue-max` (default 128MiB), and when it is under half full more WAL is fetched.

```
[global]
archive-async=y
spool-path=/path/to/spool

[global:archive-get]
process-max=2
```

It helps most where a lot of WAL is generated or latency to the repository is high, such as S3 and other object stores; in that case consider a higher `process-max`. Move files to PostgreSQL most efficiently by putting the spool path on the same filesystem as pg_wal, but not inside it, because that can confuse tools such as pg_rewind.

Monitor `<stanza>-archive-get-async.log`: it lists `get N WAL file(s) from archive`, each `found` segment, and `unable to find` when it reaches the end of the archive.

Using command sections (`[global:archive-get]`) keeps process-max out of backup and restore and allows a different value from archive-push. `archive-missing-retry` interacts with the queue: see the streaming replication skill.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Archive Get). Nothing needed removing. 

Method: documentation only; no commands were run.
