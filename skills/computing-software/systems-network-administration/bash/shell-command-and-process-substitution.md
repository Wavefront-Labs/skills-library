---
id: computing-software.systems-network-administration.bash.shell-command-and-process-substitution
name: shell-command-and-process-substitution
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-command-substitution, process-substitution, subshell-capture, backticks]
level: practitioner
status: docs-checked
description: "Capture command output with $(...) and feed commands as files with <(...) and >(...)."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command and process substitution

- `$(cmd)` replaces itself with the command's stdout, with trailing newlines deleted (embedded ones stay but may be removed by word splitting). It runs in a subshell environment, so variable changes inside do not persist.
- `local x=$(cmd)` hides cmd's status because `local` itself returns zero unless used outside a function, given an invalid name or a readonly variable. Declare, then assign: `local x; x=$(cmd)`.
- `$(< file)` is the equivalent, faster form of `$(cat file)`.
- Process substitution, `<(list)` or `>(list)` with no space between the symbol and the parenthesis, runs the list asynchronously and passes a filename as the expansion result: `diff <(sort a) <(sort b)`; `tee >(gzip > out.gz)` for output. It needs named pipes (FIFOs) or the `/dev/fd` method of naming open files.
- `while read -r l; do ...; done < <(cmd)` runs the loop in the current shell (a pipeline stage would run it in a subshell), so the loop keeps its variables.
- With `x=$(cmd)` and no command word, the exit status is that of the last command substitution performed.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Command Substitution, Process Substitution, Simple Command Expansion, Pipelines, Bourne Shell Builtins local). Confirmed each point above. Removed the claims that backticks are inferior, that quoting preserves newlines, that process substitution is absent from POSIX sh, and the NUL-byte and `read -d ''` advice; replaced the landing-page sources with the manual.
