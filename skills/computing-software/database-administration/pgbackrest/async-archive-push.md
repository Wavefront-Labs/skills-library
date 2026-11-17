---
id: computing-software.database-administration.pgbackrest.async-archive-push
name: async-archive-push
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, archive-async, archive-push, spool-path, queue]
level: advanced
status: docs-checked
description: "How asynchronous archive-push batches WAL and what archive-push-queue-max does when the queue overflows."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speed up WAL archiving without losing safety.

With `archive-async=y`, `archive-push` offloads work to a background process that looks ahead to other ready segments and pushes them in parallel. Segments are copied directly from pg_wal, and success is returned to PostgreSQL only after the WAL is safely stored.

```
[global]
archive-async=y
spool-path=/var/spool/pgbackrest

[global:archive-push]
process-max=2
```

The spool path holds status: acknowledgement files are tiny (zero bytes on success, a few hundred on error). It need not be preserved if the cluster moves; pgBackRest rechecks each segment. Keep it on a local POSIX filesystem, not NFS or CIFS, and not inside pg_wal.

Monitor with the `<stanza>-archive-push-async.log` file, e.g. after a series of `pg_switch_wal()` calls the log shows multiple WAL files pushed by parallel processes.

`archive-push-queue-max`: once exceeded, pgBackRest tells PostgreSQL the WAL was archived, then drops it, and warns in the PostgreSQL log. PITR is then impossible past that point until a new backup is taken. `archive-push-batch-size` (default 16GiB) limits WAL per async run so the queue is rechecked.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) (spool-path, archive-push-*) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Archive Push). Nothing needed removing. 

Method: documentation only; no commands were run.
