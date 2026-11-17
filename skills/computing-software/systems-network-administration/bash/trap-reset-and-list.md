---
id: computing-software.systems-network-administration.bash.trap-reset-and-list
name: trap-reset-and-list
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, trap-reset-and-list, trap-chaining, shell-scripting]
level: practitioner
status: docs-checked
description: "List, replace and reset signal traps in bash, and keep several cleanup actions in one trap handler."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing and resetting traps
**Goal:** inspect and manage traps.
```bash
trap -p                       # list trapped signals as reusable trap commands
trap -p EXIT                  # one signal
trap -P EXIT                  # only the action text (needs a signal)
trap - INT TERM               # reset to the disposition at shell start
trap '' INT                   # ignore SIGINT
trap -l                       # signal names and numbers
cleanup() { rm -f "$tmp"; kill "$bgpid" 2>/dev/null; }
trap cleanup EXIT             # one handler holds all cleanup steps
```
- `trap action sigspec` sets the handler; an action of `-` (or no action with a single sigspec) resets each signal to the value it had when the shell started; an empty string `''` makes the shell and the commands it invokes ignore the signal.
- Keep all cleanup in one function and trap that, rather than relying on several separate `trap ... EXIT` calls.
- `trap` with no arguments, or `-p`, prints the traps as commands that can be reused as shell input; `-P` shows only the action and requires a sigspec. `-p`/`-P` used in a subshell (such as command substitution) before changing any trap show the parent's traps.
- Sigspecs are names or numbers, case-insensitive, with the SIG prefix optional. `0` or `EXIT` runs at shell exit; `DEBUG`, `RETURN` and `ERR` are also accepted.
- Trapped signals that are not being ignored are reset to their original values in a subshell; non-builtin commands inherit ignored signals, so a child also ignores a signal set to `''`.
- In a non-interactive shell, signals ignored on entry cannot be trapped or reset.
- Self-check: `trap 'echo a' EXIT; trap -p EXIT` prints a trap command for EXIT.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): the trap builtin entry (actions, -, '', -l, -p, -P, subshell behaviour, EXIT/DEBUG/RETURN/ERR, ignored-on-entry rule) and the Signals section (inherited ignored signals). Removed the sed-based add_trap helper, the "second trap replaces the first" statement and the "bash 4.4+" version claim, none of which the manual states.
Method: documentation only; no commands were run.
