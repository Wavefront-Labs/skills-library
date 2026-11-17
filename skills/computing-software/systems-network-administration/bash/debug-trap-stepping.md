---
id: computing-software.systems-network-administration.bash.debug-trap-stepping
name: debug-trap-stepping
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, debug-trap-stepping, bash-step-debug, shell-scripting]
level: advanced
status: docs-checked
description: "Single-step a bash script with a DEBUG trap and read prompt, showing each command before it runs."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-stepping with the DEBUG trap
**Goal:** pause before each command interactively.
```bash
step() {
  printf '[%s:%s] %s\n' "${BASH_SOURCE[1]##*/}" "${BASH_LINENO[0]}" "$BASH_COMMAND" >&2
  read -r -p "(enter=run, q=quit) " a < /dev/tty
  [[ $a == q ]] && exit 1
}
trap step DEBUG
set -o functrace          # same as set -T: functions inherit the DEBUG trap
```
- `trap action DEBUG` runs the action before every simple command, `for`, `case` and `select` command, `((` arithmetic command, `[[` conditional, arithmetic `for` command, and before the first command in a shell function.
- `BASH_COMMAND` is the command currently being executed or about to be executed, unless the shell is running a command as the result of a trap, in which case it is the command executing at the time of the trap. `${BASH_LINENO[0]}` inside a function is the line where it was called, in `${BASH_SOURCE[1]}`.
- DEBUG and RETURN traps are normally not inherited by shell functions, command substitutions and subshells. `set -T` (`set -o functrace`) makes them inherited; setting `shopt -s extdebug` after invocation also enables function tracing, so command substitution, functions and `( command )` subshells inherit the DEBUG and RETURN traps.
- With `extdebug`, if the command run by the DEBUG trap returns a non-zero value the next command is skipped and not executed. If it returns 2 while the shell is in a function or a sourced script, the shell simulates a call to `return`.
- Read from `/dev/tty` in the handler: `read -p` shows the prompt only when input comes from a terminal, and the script's own stdin stays untouched.
- To narrow the range, run `trap step DEBUG` before the block and `trap - DEBUG` after it (an action of `-` resets the disposition to its value at shell start).

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual entries for trap (DEBUG, RETURN, `-`), the shopt extdebug entry, set -T/functrace, read -p, and the BASH_COMMAND, BASH_LINENO and BASH_SOURCE variables. Corrections: the draft said a DEBUG trap returning 2 skips the command; the manual says that under extdebug any non-zero return skips the next command and 2 simulates `return` inside a function or sourced script. The `$BASH_LINENO` expansion was changed to `${BASH_LINENO[0]}`. Removed the `bashdb` mention and the three-prompts self-check as unsourced.
