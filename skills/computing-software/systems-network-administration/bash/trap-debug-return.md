---
id: computing-software.systems-network-administration.bash.trap-debug-return
name: trap-debug-return
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, trap-debug-return, debug-trap, return-trap, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash DEBUG, RETURN and ERR traps for tracing and failure reporting, with extdebug and functrace."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DEBUG and RETURN traps
**Goal:** hook command execution and function exit.
```bash
trap 'echo "+ $BASH_COMMAND" >&2' DEBUG        # before every simple command
trap 'echo "left ${FUNCNAME[0]}"' RETURN       # when a function or sourced file returns
set -o functrace                               # functions inherit DEBUG/RETURN traps (set -T)
shopt -s extdebug                              # DEBUG trap status can skip the command
trap - DEBUG RETURN                            # remove
```
- DEBUG runs before every simple command, `for`, `case` and `select` command, `((` arithmetic command, `[[` conditional, arithmetic `for`, and before the first command in a shell function.
- RETURN runs each time a shell function, or a script run with `.` or `source`, finishes.
- ERR runs when a pipeline, list or compound command returns non-zero, under the same exceptions as `set -e` (not in `while`/`until` conditions, `if`/`elif` tests, `&&`/`||` lists except the last command, non-final pipeline commands, or `!`-inverted status). `set -E` makes ERR inherited by functions, command substitutions and subshells.
- DEBUG and RETURN traps are normally not inherited by functions, command substitutions or subshells; `set -T` (`-o functrace`) makes them inherited, and `extdebug` also enables function tracing and error tracing.
- With `extdebug`, if the DEBUG trap command returns non-zero the next command is skipped; a return value of 2 inside a function or sourced script simulates a call to `return`.
- Self-check: `trap 'echo c' DEBUG; true` prints `c` before each command.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): the trap builtin entry (DEBUG, RETURN, ERR), The Set Builtin (-T, -E), and The Shopt Builtin (extdebug). Removed the claims about heavy slowdown, `$LINENO`/`${FUNCNAME}` context and dash lacking DEBUG/RETURN, which were not checked against a page, and the "function timing" wording from the description. `$BASH_COMMAND` and `${FUNCNAME[0]}` appear in the examples only.
Method: documentation only; no commands were run.
