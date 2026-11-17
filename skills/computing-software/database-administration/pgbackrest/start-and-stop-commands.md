---
id: computing-software.database-administration.pgbackrest.start-and-stop-commands
name: start-and-stop-commands
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, stop, start, write-commands, maintenance]
level: practitioner
status: docs-checked
description: "Block pgBackRest write commands on test or promoted clusters with stop, and re-enable with start."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep non-production clusters out of the repository.

If a standby is promoted for testing or a test cluster is restored from production, `stop` prevents it from writing to repositories. It blocks the write commands `archive-push`, `backup`, `expire`, `stanza-create` and `stanza-upgrade`. `stanza-delete` is the exception.

```
pgbackrest stop
pgbackrest --stanza=demo stop
pgbackrest --stanza=demo start
```

Without `--stanza` it applies to all stanzas. A blocked backup from a repository host fails with `stop file exists for all stanzas` or `... for stanza demo` and ends with error 056, `unable to find primary cluster - cannot proceed`.

- `stop --force` terminates running pgBackRest write commands, including asynchronous archive-get (which runs again if PostgreSQL needs it).
- Stopping twice only warns that the stop file already exists.
- `start` allows new write commands; those killed or running before the stop do not restart automatically.
- A stanza stopped with `--stanza` must be started with the stanza specified.

## Checked

2026-11-08: the blocked write commands, stanza-delete exception, error 056 output, --force and per-stanza start/stop confirmed in the User Guide Starting and Stopping section and the Command Reference. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
