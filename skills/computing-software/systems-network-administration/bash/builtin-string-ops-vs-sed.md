---
id: computing-software.systems-network-administration.bash.builtin-string-ops-vs-sed
name: builtin-string-ops-vs-sed
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, builtin-string-ops-vs-sed, bash-string-builtins, shell-scripting]
level: practitioner
status: docs-checked
description: "Replace sed, cut, tr and basename forks with bash parameter expansion for substitution, case and splitting in loops."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Builtin string ops instead of sed
**Goal:** avoid a fork per line in loops.
```bash
s="Hello World"
echo "${s// /_}"          # replace all spaces      (instead of sed 's/ /_/g')
echo "${s/World/There}"   # first match
echo "${s,,} ${s^^}"      # lower / upper           (instead of tr)
echo "${s:0:5}"           # substring               (instead of cut)
IFS=, read -ra parts <<< "a,b,c"      # split       (instead of cut -d,)
[[ $s =~ ^([A-Z][a-z]+) ]] && echo "${BASH_REMATCH[1]}"
```
- `${s/pat/str}` replaces the longest match of `pat` and only the first match; `${s//pat/str}` replaces all; `${s/#pat/str}` and `${s/%pat/str}` anchor at the start or end. A null `str` deletes the match.
- `pat` is a shell pattern (glob), not a regex; use `[[ $s =~ regex ]]` with `BASH_REMATCH` for regex captures.
- With `shopt -s patsub_replacement`, an unquoted `&` in `str` is replaced by the matched text (a sed-like idiom); backslash-escape `&` for a literal one.
- `${s^^}` and `${s,,}` change the case of every character, `${s^}` and `${s,}` only the first.
- Applied to `@` or `*` (or an array subscripted with them), these expansions run on each element in turn.
- Self-check: `time` a 10k-iteration loop both ways.

## Checked
2026-11-08. Confirmed against the Bash Reference Manual: pattern substitution forms and `patsub_replacement`, case-modification expansion, substring expansion, `read -a`, here strings, `BASH_REMATCH` and glob pattern matching. Removed the per-fork timing, the sed/awk-versus-loop advice and the POSIX sh remark, which the manual does not state.
Method: documentation only; no commands were run.
