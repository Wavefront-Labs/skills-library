---
id: computing-software.systems-network-administration.restic.backup-exit-codes
name: backup-exit-codes
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, exit-codes, backup, monitoring, partial-snapshot]
level: practitioner
status: docs-checked
description: "Interpret restic backup exit codes 0, 1 and 3 and decide when a partial snapshot is acceptable in scheduled jobs."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
  - https://restic.readthedocs.io/en/stable/075_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup exit codes

For `restic backup`:

- `0`: success, a full snapshot was created.
- `1`: fatal error, no snapshot was created.
- `3`: some source files could not be read, but a snapshot was created. It is a partial snapshot.

Check the code straight after the command:

```
restic backup /path/to/data
echo $?
```

## Handling code 3

Treat it according to what you back up. For a home directory, unreadable lock files may be harmless; for a database directory, a missing file may make the snapshot useless. Log the warning lines from restic's output, alert on `3`, and do not let it silently pass as success.

## Handling anything else

The scripting reference says unknown codes must be treated as failure, because new codes may be added. In a wrapper script, branch like this:

```
case $rc in
  0) ;;
  3) warn "partial snapshot" ;;
  *) fail ;;
esac
```

The broader set of codes (2 Go runtime error, 10 no repository, 11 lock failure, 12 wrong password, 130 cancelled) is in the script-exit-codes skill.

Exit code 11 means the repository could not be locked. When scheduling restic repeatedly, make sure no other instance is already running before starting a backup.

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup) and Scripting page (075_scripting), both read in full. Confirmed: backup exit codes 0, 1 and 3 with their meanings, the table of codes 2, 10, 11, 12 and 130, the rule that unknown codes must be treated as failure, echo $?, and the advice to detect already running instances. Removed: the assumption that a lock failure usually means the previous run is still going.

Method: documentation only; no commands were run.
