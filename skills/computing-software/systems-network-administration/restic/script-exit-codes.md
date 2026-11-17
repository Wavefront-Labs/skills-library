---
id: computing-software.systems-network-administration.restic.script-exit-codes
name: script-exit-codes
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, exit-codes, scripting, repository-exists, lock, automation]
level: practitioner
status: docs-checked
description: "Handle restic exit codes 0, 1, 2, 3, 10, 11, 12 and 130 in scripts and test whether a repository already exists before running init."
sources:
  - https://restic.readthedocs.io/en/stable/075_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exit codes in scripts

| Code | Meaning |
|------|---------|
| 0 | success |
| 1 | command failed (see the command help) |
| 2 | Go runtime error |
| 3 | `backup` could not read some source data, or `forget` could not remove some snapshots |
| 10 | repository does not exist (since restic 0.17.0) |
| 11 | failed to lock the repository (since restic 0.17.0) |
| 12 | wrong password (since restic 0.17.1) |
| 130 | cancelled by SIGINT or SIGTERM |

New codes may be added, so any code you do not handle must count as failure.

## Is the repository initialised?

Instead of parsing error text, use the exit code of a cheap read:

```
restic -r /path/to/repo cat config >/dev/null 2>&1
rc=$?
```

Code `10` means the repository does not exist, so run `restic init`. Versions before 0.17.0 return code 1 instead, and code 1 is also returned for other errors such as a wrong password to `cat config`. `init` has its own guard against overwriting an existing repository, but testing first keeps scripts idempotent.

## Retry behaviour

- Code `11` means restic failed to lock the repository; check whether another restic process is running before retrying.
- Code `12` means the password is wrong. Stop and alert rather than looping.

The password can be supplied with `RESTIC_PASSWORD_FILE` or `RESTIC_PASSWORD_COMMAND` (or `RESTIC_PASSWORD`).

## Checked

Checked 2026-11-08 against the restic Scripting page (075_scripting), read in full. Confirmed: the exit code table including the since-version notes, the rule that unknown codes are failures, cat config as the repository-exists test with code 10 (code 1 before 0.17.0), init's own overwrite guard, and the password environment variables. Removed: the --retry-lock claim and the flag-versus-environment precedence remark, which the page does not state.

Method: documentation only; no commands were run.
