---
id: computing-software.systems-network-administration.bash.bash-local-scope-and-function-returns
name: bash-local-scope-and-function-returns
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, local-variables, function-return, bash-functions, dynamic-scoping, return-status, command-substitution]
level: practitioner
status: verified
description: "Scope variables with local, return data from bash functions (stdout capture, namerefs, globals) vs status with return, and avoid dynamic-scoping and subshell traps."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html
  - https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html
  - https://mywiki.wooledge.org/BashFAQ/084
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local scope and returning values

## return is a status, not a value
`return N` sets `$?` (0–255; `return 256` wraps to 0). Returning data has three idioms:
```bash
# 1. print and capture (most common; runs in a subshell)
get_stem() { local f=$1; printf '%s
' "${f##*/}"; }
stem=$(get_stem /var/log/syslog) || exit 1

# 2. nameref (bash 4.3+): no subshell, can return arrays
get_words() { local -n _out=$1; mapfile -t _out < <(printf '%s
' alpha 'beta gamma'); }
get_words words; echo "${#words[@]} words"   # 2 words

# 3. documented global (cheap, fragile)
parse_args() { OPT_VERBOSE=0; ...; }
```

## local and dynamic scoping
- Without `local`, assignments inside functions modify globals.
- Bash is dynamically scoped: a function called from another sees the caller's locals.
- `local x=$(cmd)` — the `$?` is `local`'s (always 0). Split it: `local x; x=$(cmd) || return`.
- `local -r` read-only local, `local -a`/`-A` arrays, `local -i` integer.
- Nameref name collision: `local -n out=$1` with a caller variable also named `out` (`g out`) prints `circular name reference` warnings (tested on bash 5.2) — use unlikely names (`_out`).

## Subshell traps
- Command substitution and pipelines run in subshells: variables set inside `$(f)` or `f | while read` are lost.
- `exit` inside `$(...)` exits only the subshell — check the status of the substitution.

## Verify
- [ ] `set -u` + shellcheck pass; functions called twice don't leak state (no unexpected globals: `declare -p` diff).
