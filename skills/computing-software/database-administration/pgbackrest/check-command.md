---
id: computing-software.database-administration.pgbackrest.check-command
name: check-command
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, check, validation, archiving, configuration]
level: practitioner
status: docs-checked
description: "Use check to prove archiving and repository access work, and know what it does on primaries and standbys."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: catch misconfiguration before a restore needs it.

`check` validates the configuration and the archiving setup. On a primary it forces a WAL segment through the system: the command documentation says it uses `pg_create_restore_point` and `pg_switch_wal`, then confirms the segment arrives in the repository.

```
pgbackrest --stanza=demo --log-level-console=info check
```

Output lines in the user guide show the stages: `check repo1 configuration (primary)`, then `check repo1 archive for WAL (primary)`, then the archived segment name and repository.

Where to run it:

- On the database host, it checks that host's view of the repository.
- On a standby it reports `check repo1 (standby)` and `switch wal not performed because this is a standby`.
- On a dedicated repository host, run without a stanza to check all stanzas; the guide shows each stanza checked in turn.

Run it after `stanza-create`, after any change to archive_command or repository settings, and after `stanza-upgrade`. A check can warn `unable to check pg1` when a stop file exists for the stanza (see the start and stop skill).

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the 'unable to check pg2' standby warning, which the guide does not show. 

Method: documentation only; no commands were run.
