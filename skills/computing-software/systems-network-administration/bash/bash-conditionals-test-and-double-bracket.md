---
id: computing-software.systems-network-administration.bash.bash-conditionals-test-and-double-bracket
name: bash-conditionals-test-and-double-bracket
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, conditionals, double-bracket, test-brackets, test-command, if-then, string-comparison, integer-comparison, file-tests, pattern-matching, regex-match, posix-sh, shell-scripting, rhcsa, sysadmin]
level: practitioner
status: gated
description: "Write correct bash conditionals: [ ] vs [[ ]] vs (( )), string/integer/file tests, pattern and regex matching, combining with && || and the quoting rules that avoid 'unary operator expected'."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Conditional-Constructs
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Conditional-Expressions
  - https://man7.org/linux/man-pages/man1/test.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditionals — test, [[ ]], (( )) and what each one is for

**Goal:** pick the right test construct, compare strings and numbers without surprises, and
never see `unary operator expected` again.

## 1. Three constructs
```bash
if [ "$a" = "$b" ]; then ...; fi     # POSIX test: a COMMAND; needs quoting; = not ==
if [[ $a == "$b" ]]; then ...; fi    # bash keyword: no word splitting, pattern/regex support
if (( a > b )); then ...; fi         # arithmetic: C-like operators, variables without $
```
- `[` is `/usr/bin/[`/builtin `test`; every argument is a word, so empty/unset variables
  vanish and break the syntax. `[[` parses its contents itself.
- Use `[[` in bash scripts; use `[` only for `#!/bin/sh` portability (dash, busybox).
- `[[ $a == $b ]]` treats the right side as a **glob** unless quoted. `[[ $a == "$b" ]]` is literal.

## 2. String tests
```bash
[[ -z $var ]]            # empty (or unset)
[[ -n $var ]]            # non-empty
[[ $x == foo* ]]         # glob match
[[ $x != foo ]]
[[ $x < $y ]]            # lexical (locale-dependent); inside [ ] escape: [ "$x" \< "$y" ]
[[ $x =~ ^[0-9]+$ ]]     # ERE regex; keep the pattern unquoted, or in a variable
[[ ${x,,} == yes ]]      # case-insensitive via lowercase expansion
```

## 3. Numeric tests
```bash
[[ $n -gt 5 ]]           # -eq -ne -lt -le -gt -ge: integers only
(( n > 5 && n < 10 ))    # readable; (( )) treats empty as 0, non-numeric as error/0
[[ $n =~ ^[0-9]+$ ]] || { echo "not a number" >&2; exit 2; }
```
`[[ 10 > 9 ]]` is **false** (string compare); use `-gt` or `(( ))`.

## 4. File tests
```bash
[[ -e p ]]  exists        [[ -f p ]] regular file    [[ -d p ]] directory
[[ -L p ]]  symlink       [[ -r/-w/-x p ]] perms for this user
[[ -s p ]]  size > 0      [[ -S p ]] socket  [[ -p p ]] fifo
[[ a -nt b ]] newer than  [[ a -ot b ]] older   [[ a -ef b ]] same inode
[[ -O p ]]  owned by me   [[ -G p ]] group match
```
`-e` on a dangling symlink is false (follows the link); `-L` tells you it is a link. (gated: unconfirmed, source is paywalled or blocked; this Windows/MSYS bash cannot create real symlinks, so the dangling-link behaviour was not run)

## 5. Combining
```bash
if [[ -f $cfg && -r $cfg ]] || [[ -n $FORCE ]]; then ...
if [ -f "$cfg" ] && [ -r "$cfg" ]; then ...        # POSIX: separate [ ] joined by &&; avoid -a/-o
[[ ! -d $dir ]] && mkdir -p "$dir"
if cmd; then ...  # test the EXIT STATUS of a command directly — no [ ] needed
if grep -q root /etc/passwd; then ...
```
`-a`/`-o` inside `[ ]` are ambiguous with operands like `!` or `(` (run: `[ "!" -a -f file ]` fails with "binary operator expected"); they were marked obsolescent in earlier POSIX editions and the current POSIX test page says Austin Group defect 1330 removed them. They still work in bash 5.2 (run), and ShellCheck flags them as SC2166.

## 6. Idioms
```bash
: "${VAR:?must be set}"                  # fail fast on unset
[[ $# -ge 1 ]] || { usage; exit 64; }
case $answer in [Yy]*) ok=1;; *) ok=0;; esac   # multiway: see case/select skill
```

## Failure modes
- `[: =: unary operator expected` — unquoted empty variable in `[ ]`; quote it or use `[[`.
- `[: too many arguments` — variable with spaces, unquoted.
- `[[ $a == $b ]]` true when it should not be: `$b` contains `*`/`?`; quote the right side.
- `=~` always false: pattern quoted (quoting makes it literal), or backslash classes like
  `\d` (ERE has no `\d`; use `[0-9]`).
- `if [ $? -eq 0 ]` after another command reset `$?`: test the command directly.

## Verify
- [ ] `shellcheck` reports no SC2070/SC2086/SC2166 warnings.
- [ ] Run the script with an empty and an unset variable for each test — no syntax errors.
