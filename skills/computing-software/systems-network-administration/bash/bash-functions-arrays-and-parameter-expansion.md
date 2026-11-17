---
id: computing-software.systems-network-administration.bash.bash-functions-arrays-and-parameter-expansion
name: bash-functions-arrays-and-parameter-expansion
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shell, parameter-expansion, bash-arrays, bash-functions, bash-variables, associative-arrays, declare, local, nameref, mapfile, readarray, substring, pattern-substitution, default-values, indirect-expansion, return-values, getopts, shell-scripting, lpic-1, linux]
level: practitioner
status: verified
description: "Bash functions (local, nameref, return conventions), indexed and associative arrays (mapfile, slicing, safe iteration), and the parameter-expansion forms that replace sed/basename/dirname/cut."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
  - https://www.gnu.org/software/bash/manual/html_node/Arrays.html
  - https://mywiki.wooledge.org/BashFAQ/006
  - https://mywiki.wooledge.org/BashFAQ/005
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bash functions, arrays and parameter expansion

**Goal:** stop shelling out to `sed`, `cut`, `basename` and `tr` for string work,
stop building argument lists as strings, and write functions that other people can
call without reading them.

All of this is bash (≥ 4.0; associative arrays, `mapfile`, `${var,,}`), not POSIX
`sh`. If the shebang is `#!/bin/sh`, none of §2–§3 is guaranteed.

## 1. Functions
```bash
usage() { printf 'usage: %s [-v] <host>\n' "${0##*/}" >&2; exit 2; }

# return STATUS with return; return DATA on stdout; never echo and return a value in one
get_user() {                    # $1 = user@host
  local spec=$1 user
  user=${spec%%@*}
  [[ $spec == *@* && -n $user ]] || return 1
  printf '%s\n' "$user"
}
user=$(get_user "$1") || { echo "no user in $1" >&2; exit 1; }

# return DATA by reference (bash ≥ 4.3): avoids a subshell and preserves arrays
split_host_port() {             # $1 = host:port, $2 = name of array to fill
  local -n out=$2
  out=("${1%:*}" "${1##*:}")
}
split_host_port "db.example.com:5432" hp; echo "${hp[0]} ${hp[1]}"
```
- Always `local` (including loop variables); `local` without assignment keeps the
  command's exit status visible (`local x; x=$(cmd) || ...`).
- `return` takes 0–255 (larger values wrap modulo 256: `return 256` gives 0; negative values are accepted since bash 4.3, `return -1` gives 255); `return` without a value returns the last status.
- `$FUNCNAME`, `$LINENO`, `${BASH_SOURCE[0]}` for error messages;
  `declare -f name` prints a function, `declare -F` lists them; `export -f name` makes
  it visible to child bash processes (`xargs -I{} bash -c 'name {}'`).
- Options inside functions: `local OPTIND opt; while getopts ':vf:' opt; do case $opt in
  v) verbose=1;; f) file=$OPTARG;; :) echo "-$OPTARG needs arg" >&2; return 2;; \?) return 2;; esac; done; shift $((OPTIND-1))`.
  Reset `OPTIND` locally or a second call starts parsing mid-way.
- `function name {` and `name() {` are equivalent; use the latter (POSIX). Functions
  defined in a sourced file are loaded; files run with `bash file` are not — the
  difference between `source lib.sh` and `./lib.sh`.

## 2. Indexed arrays
```bash
files=(/var/log/*.log)                      # glob → array, one element per file, spaces safe
files+=("/tmp/extra file.log")              # append
mapfile -t lines < <(grep -v '^#' conf)     # one element per line (readarray is the same)
mapfile -d '' -t paths < <(find . -name '*.conf' -print0)   # NUL-safe (-d needs bash ≥ 4.4)
IFS=, read -r -a fields <<< "$csvline"      # split a string on a delimiter

"${files[@]}"        # every element, each as one word  ← the only correct way to pass them on
"${files[*]}"        # joined into ONE word by first char of IFS (for printing)
${#files[@]}         # count
"${files[-1]}"       # last element (bash ≥ 4.3)
"${files[@]:1:2}"    # slice: 2 elements starting at index 1
"${!files[@]}"       # indices (sparse after unset!)
unset 'files[2]'     # leaves a hole; rebuild to compact: files=("${files[@]}")
for f in "${files[@]}"; do ...; done
for i in "${!files[@]}"; do echo "$i: ${files[i]}"; done
[[ ${#files[@]} -eq 0 ]] && echo "no files"
declare -p files     # debug: prints the whole array unambiguously
```
Build command lines with arrays, never strings:
```bash
args=(-rn)
[[ -n $exclude ]] && args+=(--exclude "$exclude")
grep "${args[@]}" -- "$pattern" "$dir"
```
`$@` is already an array: `"$@"` passes arguments through intact, `"$*"` does not.
`set -- "${args[@]}"` replaces the positional parameters with an array. On bash < 4.4
`"${arr[@]}"` with an empty array under `set -u` errors (fixed in 4.4, per the bash CHANGES file); write `${arr[@]+"${arr[@]}"}`
if you must support old bash/macOS.

## 3. Associative arrays (bash ≥ 4.0)
```bash
declare -A port=([http]=80 [https]=443 [ssh]=22)
port[dns]=53
echo "${port[https]}"
[[ -v port[ftp] ]] || echo "no ftp"       # key exists? (-v is bash ≥ 4.2, array elements in -v need ≥ 4.3; quote key if it has spaces)
for k in "${!port[@]}"; do printf '%s=%s\n' "$k" "${port[$k]}"; done   # unordered!
unset 'port[dns]'
# count occurrences
declare -A seen=(); while read -r ip; do seen[$ip]=$(( ${seen[$ip]:-0} + 1 )); done < <(awk '{print $1}' access.log)
```
`declare -A` is mandatory, or `arr[key]=v` makes an indexed array and the key is evaluated
as arithmetic (`m[a b]=1` fails with `syntax error in expression`; `m[http]=80` silently uses
index 0). Keys are not sorted; pipe through `sort` for output.
Cannot be exported to child processes or returned from a function except by nameref
(`local -n`). Pass to a function by name: `print_map port`, then `local -n m=$1`.

## 4. Parameter expansion — the replacements for external tools
| Need | Expansion | Instead of |
|---|---|---|
| default if unset/empty | `${v:-default}` (`${v-default}` only if unset) | |
| assign default | `${v:=default}` | |
| error if unset | `${v:?message}` | manual check |
| use alt if set | `${v:+value}` → e.g. `${DEBUG:+-x}` | if/else |
| length | `${#v}` | `wc -c` |
| substring | `${v:offset:length}`, `${v: -3}` (space before `-`) | `cut -c` |
| basename | `${path##*/}` | `basename` |
| dirname | `${path%/*}` | `dirname` |
| strip extension | `${file%.*}`; all extensions `${file%%.*}` | `sed` |
| get extension | `${file##*.}` | |
| replace first / all | `${v/old/new}`, `${v//old/new}` | `sed` |
| replace at start / end | `${v/#old/new}`, `${v/%old/new}` | |
| delete | `${v//pattern/}` | `tr -d` |
| upper / lower (bash 4) | `${v^^}`, `${v,,}`; first char `${v^}` | `tr` |
| indirect | `${!name}` (value of the var whose name is in `$name`) | `eval` |
| names by prefix | `${!PREFIX@}` | `env \| grep` |
| quote for reuse | `${v@Q}` (bash 4.4); `${v@E}` expand escapes | `printf %q` |
| trim whitespace | `v=${v#"${v%%[![:space:]]*}"}; v=${v%"${v##*[![:space:]]}"}` | `sed`/`xargs` |

Patterns in `#`, `%`, `/` are **globs** (`*`, `?`, `[..]`, plus `extglob` forms like
`+([0-9])` after `shopt -s extglob`), not regexes. `#`/`%` = shortest match,
`##`/`%%` = longest. Mnemonic: `#` is left of `$` on a US keyboard (start of string),
`%` is right of it (end).

Apply to arrays element-wise: `"${files[@]##*/}"` = all basenames,
`"${files[@]%.log}"` strips the extension from each.

Arithmetic: `$(( ))` with variables bare (`$((n * 2))`), `(( n++ ))` as a statement —
but under `set -e`, `(( n++ ))` with `n=0` returns 1 and kills the script; use
`n=$((n+1))`. Integer only; `bc -l` or `awk` for floats. `printf -v var '%05d' "$n"`
formats into a variable without a subshell; `printf '%s\n' "${arr[@]}"` prints one per
line; `printf '%q'` makes a value safe to paste into another shell.

## 5. Scope and gotchas
- Variables are global unless `local`; a function setting a loop var without `local`
  clobbers the caller's.
- `local -r` / `readonly` cannot be unset. `declare -i n` makes assignments arithmetic
  (`n='2+3'` → 5). `declare -l`/`-u` force case.
- Everything run in `$( )`, a pipeline, or `( )` is a subshell: assignments inside do not
  come back. Use `mapfile`, `read`, process substitution or namerefs.
- `[[ $v == pattern ]]` is a glob match; `[[ $v == "$pattern" ]]` is literal;
  `[[ $v =~ ^[0-9]+$ ]]` is regex with groups in `BASH_REMATCH[1..]`. Put the regex in a
  variable (`re='^([a-z]+)=(.*)$'; [[ $line =~ $re ]]`) — quoting it inline breaks it.
- `$RANDOM`, `$SECONDS`, `$EPOCHSECONDS` (5.0), `$BASHPID`, `${BASH_VERSINFO[0]}` to
  gate features: `(( BASH_VERSINFO[0] >= 4 )) || { echo 'bash 4+ required' >&2; exit 1; }`.
- `shellcheck` catches most of the above (SC2086 unquoted, SC2178/2128 array misuse,
  SC2155 local-with-command). Run it.

## Verify
- [ ] `f='/var/log/app/error.log.1'; echo "${f##*/} ${f%/*} ${f%%.*} ${f##*.}"` prints
      `error.log.1 /var/log/app /var/log/app/error 1`.
- [ ] A function filling an array via `local -n` makes the caller see all elements,
      including one containing spaces (`declare -p` shows them).
- [ ] `declare -A m; m[a b]=1; echo "${!m[@]}"` prints `a b`; without `declare -A`,
      `m[a b]=1` errors (`syntax error in expression`) and `m[word]=1` assigns index 0.
- [ ] `shellcheck` on the script reports no SC2086/SC2128/SC2155 warnings.
