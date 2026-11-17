---
id: computing-software.database-administration.dragonfly.acl-log-and-dryrun
name: acl-log-and-dryrun
category: computing-software
field: database-administration
product: dragonfly
tags: [acl-log, acl-dryrun, acllog-max-len, security-events, dragonfly]
level: practitioner
status: docs-checked
description: "Audit failed authentication and denied commands with ACL LOG, size the per-thread log with acllog_max_len, and test rules with ACL DRYRUN."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/acl/log.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/acl/dryrun.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/acl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## ACL LOG

`ACL LOG [count | RESET]` lists recent security events: failed `AUTH` or `HELLO` authentication, and commands denied by ACL rules. Ten entries are returned by default; `RESET` clears the log. Entries show reason, object, username, age-seconds, client-info and timestamp-created.

Sizing: `--acllog_max_len` (default 32) is **per thread**, because Dragonfly keeps one log per execution thread. The total is the flag times the number of threads. With 4 threads and `--acllog_max_len=8` up to 32 entries are stored. When a thread's log is full the oldest entry is evicted.

## ACL DRYRUN

`ACL DRYRUN username command [arg ...]` simulates a command for a user without executing it or enabling the user:

```shell
dragonfly> ACL SETUSER mike >mypass +GET -SET
OK
dragonfly> ACL DRYRUN mike SET
"This user has no permissions to run the 'SET' command"
```

It replies `OK` if allowed, otherwise an error string.

Both commands are `@admin`, `@slow`, `@dangerous`.

## Checked

2026-11-04. Confirmed in the ACL LOG page (events, default ten entries, RESET, entry fields), the ACL DRYRUN page (syntax, example, ACL categories), the ACL guide (per-thread log, 4 threads x 8 = 32) and the flags page (`acllog_max_len` default 32). Nothing removed.

Method: documentation only; no commands were run.
