---
id: computing-software.systems-network-administration.bash.bash-case-modification-and-transformations
name: bash-case-modification-and-transformations
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, case-modification, parameter-transformation, parameter-expansion, quoting, at-q, uppercase-lowercase]
level: practitioner
status: verified
description: "Transform values in bash without external tools: ^^ ,, ~~ case changes, ${var@Q} shell-quoting, @E, @P, @A and @U/@L, with uses for safe logging and generated commands."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case modification and @ transformations

## Case
```bash
name="web Server"
echo "${name^^}"    # WEB SERVER
echo "${name,,}"    # web server
echo "${name^}"     # Web Server (first char)
echo "${name^^[aeiou]}"   # pattern: only vowels uppercased
echo "${name~~}"    # toggle case (works in 5.2; rarely known, so avoid in shared scripts)
arr=(a b c); echo "${arr[@]^^}"   # applies to every element
[[ ${answer,,} == y* ]] && echo yes     # case-insensitive compare
```
Bash 5.1+ (bash NEWS): `${var@U}`, `${var@u}` (first), `${var@L}` (run on 5.2.37: `abc` gives `ABC Abc abc`).

## Transformations (bash 4.4+)
| Op | Result |
|---|---|
| `${var@Q}` | value quoted so it can be reused as shell input |
| `${var@E}` | expand backslash escapes like `$'...'` |
| `${var@P}` | expand as a prompt string (PS1 escapes) |
| `${var@A}` | assignment statement recreating the variable with attributes; for arrays use `${arr[@]@A}` (plain `${arr@A}` shows element 0 only: `declare -ax ar='1'`) |
| `${var@a}` | attribute flags (`ax` for exported array) |
| `${arr[@]@K}` | (5.1) quoted key/value pairs; with `[@]` (without it an associative array expands to nothing). `@k` (5.2) gives separate words. Output for `m=([k]=v [j]=w)`: `k "v" j "w"` |

```bash
args=(--name "my file" "it's")
echo "running: mycmd ${args[*]@Q}"     # running: mycmd '--name' 'my file' 'it'\''s'  — copy-pasteable log
printf -v cmd '%q ' mycmd "${args[@]}" # older equivalent
```

## Gotchas
- Locale affects case mapping (Turkish i); use `LC_ALL=C` for ASCII-only identifiers.
- macOS ships bash 3.2 — none of this works there (use `tr`).
- `@Q` output is for bash; don't feed it to other shells.

## Verify
- [ ] `bash --version` ≥ 4.4 asserted in scripts that use @ transformations; logged commands paste-run identically.
