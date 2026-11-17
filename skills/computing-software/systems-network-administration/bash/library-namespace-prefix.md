---
id: computing-software.systems-network-administration.bash.library-namespace-prefix
name: library-namespace-prefix
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, library-namespace-prefix, function-prefix, shell-scripting]
level: advanced
status: docs-checked
description: "Avoid name clashes in bash libraries with function and variable prefixes, local variables, and source guards."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespacing library functions
**Goal:** libraries that coexist.
```bash
# lib/log.sh
[[ -n ${_LOG_SH_LOADED-} ]] && return 0; _LOG_SH_LOADED=1
LOG_LEVEL=${LOG_LEVEL:-info}
log_info()  { printf '%s INFO %s\n' "$(date +%T)" "$*" >&2; }
log_error() { printf '%s ERROR %s\n' "$(date +%T)" "$*" >&2; }
```
- Variables are shared between a function and its caller unless declared `local`, so declare function-scope variables `local` and give library globals a prefix (`LOG_`) so they cannot clobber the caller's names.
- A sourced file runs in the current shell (`source file` or `. file`), so everything it defines lands in the caller's namespace. `return` stops a sourced file and returns control to the caller, which allows a source guard: the second load returns at once and does not redefine functions.
- Prefixes such as `log_` are a convention; the shell does not enforce them. Use an underscore-led name for private helpers by convention only.
- Do not change shell options (`set -e`, `shopt`) in a library: they apply to the caller, because the file is executed in the caller's shell context.
- Self-check: sourcing the file twice produces no error and defines each function once.

## Checked
2026-11-09. Confirmed in the bash manual: `local` scoping, `.` / `source` run in the current shell context, `return` from a sourced file. Removed: the `declare -F` listing advice, the `log::info` namespace-separator style and the claim that colons are invalid in POSIX function names (not on the cited pages), and the `readonly` double-load remark.
Method: documentation only; no commands were run.
