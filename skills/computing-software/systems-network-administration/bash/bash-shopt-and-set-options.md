---
id: computing-software.systems-network-administration.bash.bash-shopt-and-set-options
name: bash-shopt-and-set-options
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shopt, set-builtin, nullglob, globstar, extglob, shell-options, inherit-errexit]
level: practitioner
status: verified
description: "Know and set the bash options that change script behaviour: shopt nullglob/failglob/globstar/extglob/lastpipe/inherit_errexit and set -o noclobber/nounset/pipefail."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html
  - https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shopt and set options

## Inspect
`shopt` (all, on/off), `shopt -p` (re-usable commands), `set -o`, `echo $-` (single-letter flags active),
`shopt -q nullglob && echo on`.

## shopt options worth knowing
| Option | Effect | Use |
|---|---|---|
| `nullglob` | unmatched glob expands to nothing (not the literal `*.log`) | loops over files that may not exist |
| `failglob` | unmatched glob is an error | strict scripts |
| `globstar` | `**` matches recursively | `for f in src/**/*.py` |
| `extglob` | `!(x)`, `@(a|b)`, `+(..)` patterns | `rm -- !(*.keep)` |
| `dotglob` | `*` includes dotfiles | copying whole dirs |
| `nocaseglob` / `nocasematch` | case-insensitive globs / `[[ == ]]` and `case` | |
| `lastpipe` | last pipeline stage runs in the current shell (has no effect while job control is active, e.g. interactive shells; works in scripts; tested with `set +m`) | `cmd | while read x; do n=$((n+1)); done` keeps `n` |
| `inherit_errexit` | `set -e` applies inside `$(...)` | strict mode |
| `histappend`, `checkwinsize`, `cdspell`, `autocd` | interactive niceties | `.bashrc` |

## set options
`set -e` (errexit), `-u` (nounset), `-o pipefail`, `-x` (xtrace), `-C`/`-o noclobber` (`>` won't overwrite; `>|` forces),
`-f` (disable globbing), `-o posix`, `-o vi` (vi line editing).

## Scope
Options are per-shell; set them at the top of scripts. In functions, change and restore:
```bash
f() { local -; set -f; ...; }          # 'local -' (bash 4.4+) restores set options on return
old=$(shopt -p nullglob); shopt -s nullglob; files=(*.csv); eval "$old"
```

## Gotchas
- `extglob` must be enabled before the line containing the pattern is parsed (not inside the same compound command).
- `nullglob` makes `ls *.x` with no match run plain `ls` — list everything.
- `globstar` follows symlinks to dirs in bash < 4.3.

## Verify
- [ ] `shopt -p` / `set -o` in the script's environment show what you expect; shellcheck clean.
