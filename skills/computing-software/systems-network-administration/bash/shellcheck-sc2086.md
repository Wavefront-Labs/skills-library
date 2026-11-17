---
id: computing-software.systems-network-administration.bash.shellcheck-sc2086
name: shellcheck-sc2086
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shellcheck-sc2086, sc2086, shell-scripting]
level: practitioner
status: docs-checked
description: "Fix ShellCheck SC2086 double-quote warnings correctly, and decide when intentional splitting needs an array or a disable."
sources:
  - https://www.shellcheck.net/wiki/SC2086
  - https://www.shellcheck.net/wiki/SC2046
  - https://www.shellcheck.net/wiki/SC2068
  - https://www.shellcheck.net/wiki/SC2155
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixing SC2086 unquoted variables
**Goal:** resolve "Double quote to prevent globbing and word splitting".
```bash
echo $1               # SC2086
echo "$1"             # fix
for i in "$@"; do :; done          # or: for i; do
options=(-j 5 -B)                  # intentional split: use an array (bash, ksh, zsh)
make "${options[@]}" file
bash ${debug:+"-x"} script         # optional argument: alternate-value expansion
```
- An unquoted `$1` is split by IFS (spaces, tabs, line feeds) and each piece is expanded as a glob. Quoting prevents word splitting and globbing and stops the script breaking on spaces, line feeds and glob characters.
- Strictly only the expansions need quoting, but quoting a whole composite argument is canonical: `"$HOME/$dir/dist/bin/$file"`. Keep globs and brace expansions outside the quotes: `"$HOME/$dir/src"/*.c` expands, `"$HOME/$dir/src/*.c"` does not.
- `$( )` starts a new quoting context: variables inside must be quoted independently.
- To split on spaces deliberately: an array in bash, ksh or zsh, or a function that builds arguments with `set --` in POSIX sh. `set -f` disables globbing; `IFS=''` disables word splitting.
- Quoting an empty optional argument does not work (`"$debug"` becomes one empty argument, `$debug` becomes none): use a zero-or-one element array or `${debug:+"-x"}`.
- Related warnings: SC2046 (quote `$(...)` to avoid word splitting), SC2068 (double quote array expansions), SC2155 (declare and assign separately to avoid masking return values).
- The page notes the warning can be ignored on a case-by-case basis, only where splitting is genuinely intended.
- Self-check: ShellCheck reports no SC2086 for the script.

## Checked
2026-11-09. Confirmed against the SC2086, SC2046, SC2068 and SC2155 wiki pages (title, rationale, composite quoting, arrays, POSIX function alternative, `set -f`, `IFS=''`, `${var:+...}`). Removed: the `rm --` example and `rsync` example (not on the pages), the claim that `$(( ))` and `[[ ]]` need no quoting, the disable-directive syntax and placement rule, and the `shellcheck -S warning` self-check.
Method: documentation only; no commands were run.
