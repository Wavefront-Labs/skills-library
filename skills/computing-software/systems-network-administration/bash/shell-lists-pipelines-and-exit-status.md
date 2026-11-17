---
id: computing-software.systems-network-administration.bash.shell-lists-pipelines-and-exit-status
name: shell-lists-pipelines-and-exit-status
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-command-lists, pipelines, and-or-lists, exit-codes, pipestatus]
level: practitioner
status: docs-checked
description: "Combine commands with pipes, &&, || and ; and read exit statuses (including PIPESTATUS and pipefail) correctly."
sources: ["https://www.gnu.org/software/bash/manual/bash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipelines, lists and exit status

- Zero means success, non-zero failure; `$?` holds the last command's status. 126 means found but not executable, 127 not found, and a command killed by fatal signal N gives 128+N (so SIGINT, signal 2, gives 130). All builtins return 2 for incorrect usage.
- `a && b` runs b only if a returned zero; `a || b` runs b only if a returned non-zero; `a ; b` runs both in turn. An AND or OR list returns the status of the last command executed, so `a && b || c` is not if/else: c also runs if b fails. Use `if a; then b; else c; fi`.
- A pipeline's status is its last command's, unless `set -o pipefail` (then the rightmost command that exited non-zero, or zero if all succeeded; off by default). A leading `!` negates the status. `${PIPESTATUS[@]}` holds the status of every command in the most recent foreground pipeline (read it immediately, as the next command resets it).
- Each command in a pipeline runs in its own subshell, so `echo x | read v` leaves `v` unset in your shell. Use `read v < <(echo x)`, or `shopt -s lastpipe` when job control is not active (scripts).
- `set -e` (errexit) and the `ERR` trap ignore failures in the same places: tests after `if`/`elif`/`while`/`until`, any `&&`/`||` command but the last, any pipeline command but the last (unless pipefail), and `!`-inverted commands.
- Group: `{ a; b; } > out` runs in the current shell with no subshell (a `;` or newline before `}` is required); `( a; b )` runs in a subshell.
- Return meaningful codes from your own scripts: `exit 0` success, non-zero for errors; `exit 2` for usage matches the builtin convention; document codes in `--help`.

## Checked
2026-11-08. Confirmed in the GNU Bash manual: Exit Status (0, 126, 127, 128+N, builtin usage 2), AND/OR lists, pipeline status and pipefail, PIPESTATUS, lastpipe, `{ list; }` rules, the ERR trap conditions that match errexit. Removed: the named signal numbers 137 and 143 as hard facts (derivable from 128+N but not listed) and "exit 1 for errors" as a convention claim.
Method: documentation only; no commands were run.
