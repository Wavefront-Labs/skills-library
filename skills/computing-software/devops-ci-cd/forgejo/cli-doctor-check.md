---
id: computing-software.devops-ci-cd.forgejo.cli-doctor-check
name: cli-doctor-check
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [forgejo-doctor, doctor-check, doctor-fix, doctor-list]
level: practitioner
status: docs-checked
description: "Diagnose and optionally repair an instance with forgejo doctor check, selecting checks and writing a log file."
sources:
  - https://forgejo.org/docs/latest/admin/command-line/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`forgejo doctor check` diagnoses problems with the current instance according to its configuration. Some problems can be fixed by changing the database or data storage.

Options:

- `--list`: print the available checks.
- `--default`: run the default checks; this is the behaviour when neither `--run` nor `--all` is given.
- `--run <check>`: run the named check, repeatable; combined with `--default` the defaults also run.
- `--all`: run every available check.
- `--fix`: automatically fix what can be fixed.
- `--log-file <name>`: where to write the log; no verbose output by default; `-` prints to stdout.
- `--color`, `-H`: colored output.

The global `--config`, `--custom-path` and `--work-path` options let you point the command at a particular installation.

Example: list the checks with `forgejo doctor check --list`. The upgrade guide has you run `forgejo doctor check --all --log-file /path/to/doctor.log` before upgrading and make sure it reports no problem.

## Checked

2026-11-04. Confirmed against the Forgejo command-line page (doctor and doctor check help text) and the Upgrade page. Removed: the advice to run it after an upgrade, to read results before adding --fix and to back up first, none of which the pages state.

Method: documentation only; no commands were run.
