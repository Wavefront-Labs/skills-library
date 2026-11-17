---
id: computing-software.systems-network-administration.bash.shell-function-libraries-and-sourcing
name: shell-function-libraries-and-sourcing
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-source-libraries, shell-functions, dot-command, include-guards, main-function]
level: practitioner
status: docs-checked
description: "Organise shell code into functions and sourced libraries with include guards and a main entry point."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions and libraries

- `source file` (bash) or `. file` reads and executes commands from the file in the current shell context. If the filename has no slash, bash searches `PATH` (or the directories given with `-p`) and, outside POSIX mode, the current directory if it is not found in `PATH`. So give the path explicitly, relative to the script directory rather than the cwd: `. "$script_dir/lib/log.sh"`. The file need not be executable.
- Library files should define functions and have no side effects on load. `return` stops executing a sourced file and hands a status to its caller, which makes an include guard possible: `[ -n "${_LIB_LOG_SH:-}" ] && return; _LIB_LOG_SH=1`.
- Structure each script: `usage()`, helper functions, `main()`, then `main "$@"`.
- Variables are shared between a function and its caller unless declared with the `local` builtin; locals are visible only to that function and the commands it invokes. Prefix library globals.
- `return n` gives a function (or sourced file) a status; only the least significant 8 bits of n are used. Write results to stdout; to avoid a command-substitution subshell, assign through a nameref (`local -n out=$1`; a nameref makes the name refer to the variable whose name it holds) or `printf -v`.
- `export -f` marks functions to be passed to subsequently executed commands in the environment; do not use it across trust boundaries.
- Command substitution `$(...)` runs in a subshell, so a function that must change the caller's directory or variables must run in the current shell, not inside `$(...)`.
- Namespace library functions by a prefix (`log_info`), keep exported variable names distinct, and keep style decisions consistent across a codebase.

## Checked
2026-11-09. Confirmed in the bash manual: `.` / `source` search behaviour, `return` in sourced files and 8-bit status, `local`, `printf -v`, nameref, `export -f`, command substitution in a subshell. Removed: the claim that a missing file makes a non-interactive POSIX shell exit, that `local` is not strictly POSIX, the `[ -r ]` check rationale, the naming-case conventions presented as rules, and the POSIX root URL (a stub page).
Method: documentation only; no commands were run.
