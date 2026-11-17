---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-runscript-pre-post-jobs
name: bacula-runscript-pre-post-jobs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula-runscript, bacula, bareos, pre-freeze-script, database-backup, bacula-dir]
level: practitioner
status: docs-checked
description: "Run commands before and after Bacula/Bareos jobs with RunScript: client vs director side, RunsWhen, FailJobOnError, shell handling, and job variables."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html
  - https://docs.bareos.org/Configuration/Director.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula RunScript (pre/post job commands)

## Syntax (Job or JobDefs resource in bacula-dir.conf)
```
Job {
  Name = "pg01-db"
  JobDefs = "DefaultJob"
  Client = pg01-fd
  FileSet = "pg-dumps"
  RunScript {
    RunsWhen = Before
    RunsOnClient = Yes
    FailJobOnError = Yes
    Command = "/usr/local/sbin/pg_dump_all.sh %l"
  }
  RunScript {
    RunsWhen = After
    RunsOnClient = Yes
    RunsOnFailure = Yes
    Command = "/usr/local/sbin/cleanup_dumps.sh"
  }
  RunScript {
    RunsWhen = After
    RunsOnClient = No           # runs on the Director host
    RunsOnSuccess = Yes
    Command = "/usr/local/bin/notify.sh %n %e %b"
  }
}
```
Shorthands: `ClientRunBeforeJob`, `ClientRunAfterJob`, `RunBeforeJob`, `RunAfterJob`,
`RunAfterFailedJob`. The Client shorthands run on the client; the others on the Director.
With `ClientRunBeforeJob`, a command error discards other remote runscripts; use the `RunScript`
syntax to be sure all commands are sent and executed.

## Options (Bacula manual defaults)
| Directive | Meaning |
|---|---|
| `RunsWhen` | Before, After, Always, AfterVSS, AtJobCompletion (Bacula manual) |
| `RunsOnClient` | Yes (default; File Daemon host) / No (Director). Jobs with no client (Copy, Migration, Admin) need No |
| `RunsOnSuccess` | default Yes |
| `RunsOnFailure` | default No |
| `FailJobOnError` | default Yes: job fails if the script returns non-zero |
| `Command` vs `Console` | program to run vs a console command sent to the Director |

`AfterVSS` runs the script just after snapshot initialisation (Windows).

## Substitution variables
`%b` job bytes, `%c` client name, `%d` daemon name, `%e` job exit status, `%F` job files, `%f`
job FileSet (director side only), `%i` JobId, `%j` unique job id, `%l` job level, `%n` job
name, `%t` job type, `%v` volume name (director side only). `%e` yields OK, Error, Fatal Error,
Canceled, Differences or Unknown term code, so quote it on a command line.

## Shell handling
Output on standard output goes into the job report. The command string is parsed and run with
no shell interpretation: for redirection or pipes call a shell script, or use
`"sh -c \"your commands go here\""`. Use a full path or a name found in `$PATH`.

## Database dump pattern
Before script dumps to a local directory included in the FileSet; After script removes old
dumps. With `FailJobOnError = Yes` a failing dump script fails the job rather than backing up
a stale dump.

## Checked
2026-11-01. Confirmed in the Bacula 15.0 manual (Configuring the Director, RunScript) and the
Bareos Director configuration page: option table with defaults, shorthand table, substitution
characters (corrected %f, %F, %j, %d, %v), %e values, no-shell-interpretation note, AfterVSS,
ClientRunBeforeJob note. Removed: daemon-user and PATH remarks, MaxRunTime interaction, database
plugin alternatives, bconsole verification line, which these pages do not state.
Method: documentation only; no commands were run.
