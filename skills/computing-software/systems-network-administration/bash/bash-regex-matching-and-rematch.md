---
id: computing-software.systems-network-administration.bash.bash-regex-matching-and-rematch
name: bash-regex-matching-and-rematch
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, bash-rematch, bash-regex, regex-operator, double-bracket, ere, capture-groups, input-validation, string-extraction, shell-scripting, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Match and extract with bash's =~ operator: ERE syntax, capture groups in BASH_REMATCH, storing patterns in variables, anchoring, case-insensitivity, and the quoting rules that break matches."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Conditional-Constructs
  - https://man7.org/linux/man-pages/man7/regex.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# =~ and BASH_REMATCH — regex without spawning grep/sed

**Goal:** validate input and pull fields out of strings in pure bash, correctly quoted, with
captures.

## 1. Basic form
```bash
if [[ $ip =~ ^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$ ]]; then
    echo "octets: ${BASH_REMATCH[1]} ${BASH_REMATCH[2]} ${BASH_REMATCH[3]} ${BASH_REMATCH[4]}"
fi
```
- Only inside `[[ ]]`. The right side is POSIX **ERE** (`+ ? | () {n,m}` work; no `\d`
  (does not match digits); `\w`/`\s` are libc extensions that did not match on the msys build tested — use `[[:digit:]]`, `[[:alnum:]_]`).
- `BASH_REMATCH[0]` is the whole match, `[1..n]` the groups. It is overwritten by every
  successful match — copy it immediately.
- Unanchored by default: `[[ abc123 =~ [0-9]+ ]]` matches. Anchor with `^`/`$`.

## 2. Quoting — the rule everyone trips over
```bash
[[ $s =~ ^foo.*$ ]]        # works: pattern unquoted
[[ $s =~ "^foo.*$" ]]      # quoted = LITERAL string "^foo.*$"; almost never what you want
re='^([a-z]+)=([^ ]+)$'    # best practice: pattern in a variable
[[ $line =~ $re ]]
[[ $s =~ ^foo" bar"$ ]]    # quote only the parts that need literal spaces/metachars
```
Storing the regex in a variable avoids both the quoting problem and the bash 3.2
compatibility quirk (`compat31`) around escaping.

## 3. Extraction idioms
```bash
re='^([^:]+):([^:]*):([0-9]+):([0-9]+):'
while IFS= read -r l; do [[ $l =~ $re ]] && echo "user=${BASH_REMATCH[1]} uid=${BASH_REMATCH[3]}"; done < /etc/passwd

# key=value with optional quotes
re='^([A-Za-z_][A-Za-z0-9_]*)="?([^"]*)"?$'
[[ 'NAME="Rocky Linux"' =~ $re ]] && printf '%s -> %s\n' "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"

# version numbers
re='([0-9]+)\.([0-9]+)(\.([0-9]+))?'
[[ $(uname -r) =~ $re ]] && (( BASH_REMATCH[1] >= 6 )) && echo "6.x kernel"

# global matching: loop stripping the matched prefix
s='a=1 b=2 c=3'; re='([a-z])=([0-9])'
while [[ $s =~ $re ]]; do echo "${BASH_REMATCH[1]}:${BASH_REMATCH[2]}"; s=${s#*"${BASH_REMATCH[0]}"}; done
```

## 4. Options
```bash
shopt -s nocasematch   # case-insensitive =~ and case; unset afterwards
[[ $x =~ ^[[:space:]]*# ]] && echo comment
```
Locale affects `[a-z]` ranges and `[[:alpha:]]`; use `LC_ALL=C` for byte-exact behaviour.

## 5. When not to use it
- Multi-line text or files → `grep -E`, `sed -E`, `awk`.
- Need substitutions → `${var//pattern/repl}` (glob) or `sed`.
- Performance on 100k+ iterations is acceptable (no fork), but awk is still faster for bulk.

## Failure modes
- Always false: pattern quoted; `\d` used; `\{` where you meant a repetition count (`\{` matches a literal brace; use bare `{n,m}`). A bare `{` that is not a valid repetition is a regex error (status 2).
- "syntax error in conditional expression": unescaped `)` or `|` in the pattern — put it
  in a variable.
- Captures empty after a later test: `BASH_REMATCH` overwritten; copy first.
- Works interactively, fails in script: `nocasematch` or `extglob` set in your shell only.
- `=~` inside `[ ]` or `test`: not supported — `[[` only.

## Verify
- [ ] Feed a known-good and known-bad sample; exit status 0/1 respectively (`[[ ... ]]; echo $?`).
- [ ] `declare -p BASH_REMATCH` shows the expected groups right after the match.
