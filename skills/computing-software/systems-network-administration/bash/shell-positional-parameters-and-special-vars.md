---
id: computing-software.systems-network-administration.bash.shell-positional-parameters-and-special-vars
name: shell-positional-parameters-and-special-vars
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-special-parameters, positional-parameters, shift, dollar-at-vs-star]
level: practitioner
status: docs-checked
description: "Use $@, $*, $#, $?, $$, $!, $0 and shift correctly, and set IFS locally."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special parameters

- `$1..$9`, `${10}` positional arguments (braces are required for more than one digit); `$#` count; `$@`/`$*` all positionals; `$0` script name; `$?` exit status of the last command; `$$` shell PID; `$!` PID of the job most recently put in the background; `$-` current option flags; `$_` last argument of the previous simple command.
- Quoting: `"$@"` is equivalent to `"$1" "$2" ...` (one word each) and expands to nothing when there are no positionals; `"$*"` is one word joined with the first character of IFS.
- `shift [n]` shifts positionals left by n (default 1); n must be at most `$#`, otherwise the status is non-zero. Loop: `while [ $# -gt 0 ]; do case $1 in ... esac; shift; done`.
- `set -- a b c` sets positionals; `set --` with no arguments unsets them.
- Required argument with message: `: "${1:?usage: $0 file}"`; default: `${1:-default}`; `${var:?}` writes an error and exits a non-interactive shell when unset or null.
- In a subshell `$$` still expands to the invoking shell's PID; `$BASHPID` gives the current Bash process's PID.
- Change IFS only locally: an assignment before a command, as in `IFS=, read -ra a <<< "$s"`, affects only the environment seen by that command; or use `local IFS` in a function.
- `RANDOM` (integer 0 to 32767), `SECONDS`, `LINENO`, `FUNCNAME`, `BASH_SOURCE` and `BASHPID` are Bash variables; RANDOM and BASHPID are listed among the features Bash adds over the Bourne shell.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Special Parameters, Shell Parameter Expansion, The Set Builtin, Bourne Shell Builtins shift, Simple Command Expansion, Bash Variables). Confirmed each special parameter, `shift` rules, `set --`, `:?`, `$$` in subshells, BASHPID and RANDOM range. Removed the `$$`-as-temp-file and mktemp advice, the save-and-restore IFS recipe and the function-positional claim, which were not confirmed; source landing pages replaced by the manual itself.
