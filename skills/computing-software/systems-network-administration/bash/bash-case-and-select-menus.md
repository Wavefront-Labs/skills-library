---
id: computing-software.systems-network-administration.bash.bash-case-and-select-menus
name: bash-case-and-select-menus
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, case-statement, select-menu, select-loop, ps3, pattern-matching, fallthrough, argument-dispatch, interactive-menu, shell-scripting, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Dispatch on patterns with case (globs, alternation, ;;& fallthrough, extglob) and build numbered interactive menus with select/PS3, including validation and quit handling."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Conditional-Constructs
  - https://www.gnu.org/software/bash/manual/bash.html#Pattern-Matching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case and select — multiway dispatch and quick menus

**Goal:** replace if/elif chains on a single value with `case`, and give operators a safe
numbered menu with `select` without hand-rolling input parsing.

## 1. case — pattern dispatch
```bash
case $1 in
    start|up)        start_svc ;;
    stop|down)       stop_svc ;;
    restart)         stop_svc; start_svc ;;
    -h|--help|'')    usage; exit 0 ;;
    -*)              echo "unknown option $1" >&2; exit 64 ;;
    *.tar.gz|*.tgz)  tar -xzf "$1" ;;
    [0-9]*)          echo "numeric" ;;
    *)               echo "unknown: $1" >&2; exit 64 ;;
esac
```
- Patterns are **globs**, not regex: `*`, `?`, `[a-z]`, `|` alternation. The word is not
  split or glob-expanded, so `case $f in` is safe unquoted (quoting is fine too).
- First match wins; `*)` last as default.
- `shopt -s extglob` enables `@(a|b)`, `!(x)`, `+(pattern)`; `shopt -s nocasematch` for
  case-insensitive matching.
- Put `shopt -s extglob` on its own line before the `case`: on the same line bash 5.2.37 fails with "syntax error near unexpected token `(`" because the whole line is parsed before the option takes effect.
- Terminators: `;;` stop; `;&` fall through into the next body unconditionally; `;;&`
  continue testing later patterns.

```bash
case $os in
    rhel|rocky|alma) pkg=dnf ;;&
    rhel)            echo "subscription needed" ;;
    debian|ubuntu)   pkg=apt ;;
esac
```

## 2. Common uses
```bash
# option parsing without getopts
while [[ $# -gt 0 ]]; do
    case $1 in
        -v) verbose=1 ;;
        -o) out=$2; shift ;;
        --out=*) out=${1#--out=} ;;
        --) shift; break ;;
        *)  break ;;
    esac; shift
done

# yes/no prompts
read -rp "Continue? [y/N] " ans
case ${ans,,} in y|yes) ;; *) exit 1 ;; esac

# detect distro family
case $(. /etc/os-release; echo "$ID_LIKE $ID") in *rhel*|*fedora*) ...;; *debian*) ...;; esac
```

## 3. select — numbered menus
```bash
PS3='Pick an environment: '
select env in dev staging prod quit; do
    case $env in
        dev|staging|prod) echo "deploying to $env"; break ;;
        quit)             exit 0 ;;
        *)                echo "invalid choice: $REPLY" ;;
    esac
done
```
- `select` prints the list numbered, shows `$PS3`, reads a number into `$REPLY` and sets the
  variable to the matching word (empty for bad input). It loops forever — `break` yourself.
- Items come from a word list or array: `select f in "${files[@]}"`.
- Ctrl-D (EOF) exits the loop with the variable unchanged; handle `[[ -z $env ]]` after.
- Columns are chosen from `$COLUMNS`/`$LINES`; set `COLUMNS=1` for a single column list.

```bash
select f in *.conf; do [[ -n $f ]] && { vim "$f"; break; }; done
```

## 4. Case vs if vs associative array
- One variable against several literal/glob patterns → `case`.
- Mixed conditions (file tests, numeric) → `if`.
- Key → value mapping (`pkg[rhel]=dnf`) → `declare -A` and `${map[$k]:-default}`.

## Failure modes
- `case` never matches a path: pattern unquoted with spaces or you expected regex (`.*`).
- Branch runs for everything: a `*)` placed before specific patterns.
- `select` shows the prompt but no menu: list empty (glob matched nothing, array unset).
- Menu numbers misaligned after a resize: `select` reads `COLUMNS` at loop start; re-enter.
- Fallthrough `;&` used accidentally instead of `;;` — bodies run unexpectedly.

## Verify
- [ ] Every input class you care about (empty, `-x`, path with spaces, number) hits the intended branch — test with `set -x`.
- [ ] `select` loop exits on both a valid choice and Ctrl-D.
