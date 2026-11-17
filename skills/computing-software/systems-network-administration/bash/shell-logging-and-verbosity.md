---
id: computing-software.systems-network-administration.bash.shell-logging-and-verbosity
name: shell-logging-and-verbosity
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-logging, stderr-logging, log-levels, timestamps]
level: practitioner
status: docs-checked
description: "Add logging to bash scripts: stderr for diagnostics, a log helper, printf %(fmt)T timestamps, tee via process substitution."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging

- Write diagnostics to stderr (`>&2`) and results to stdout, so pipelines and `$(...)` captures (which take standard output) stay clean.
- Small helper: `log() { printf '%s %s %s\n' "$(date -u +%FT%TZ)" "$1" "${*:2}" >&2; }`. In bash, `printf '%(%FT%T%z)T\n' -1` prints the current time with no `date` fork: `%(datefmt)T` formats an integer of seconds since the epoch with `strftime(3)`, `-1` means the current time and `-2` the time the shell was invoked; with no argument it behaves as if `-1` were given.
- Levels via a variable: `(( VERBOSE >= 1 )) && log INFO ...`; map `-v` / `-q` flags to it.
- Capture everything to a file and the terminal: `exec > >(tee -a "$LOG") 2>&1`. Process substitution lets a process's input or output be referred to by a filename, and the substituted process runs asynchronously, so wait or flush before the script exits.
- Never log secrets. `set -x` prints a trace of commands after expansion to standard error (prefixed with the expanded `PS4`), so credentials appear in it: use `set +x` around commands that handle them.

## Checked
2026-11-09. Confirmed in the bash manual: `printf` `%(datefmt)T` with `-1` / `-2`, process substitution, `set -x` and `PS4`, `>&` redirection of stderr. Removed: the bash 4.2 version tag, `NO_COLOR` and `[ -t 2 ]` colour advice, `logger` and `journalctl` usage, and the cron/systemd mail and journal remarks, none of which the cited pages state; the POSIX root URL (a stub page) was dropped from sources.
Method: documentation only; no commands were run.
