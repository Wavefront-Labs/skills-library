---
id: computing-software.systems-network-administration.bash.globbing-extglob-and-brace-expansion
name: globbing-extglob-and-brace-expansion
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, globbing, extglob, brace-expansion, globstar, nullglob, dotglob, nocaseglob, failglob, character-classes, filename-expansion, shell-scripting, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Control filename expansion: glob syntax and character classes, shopt globstar/nullglob/dotglob/failglob/nocaseglob, extglob patterns, brace expansion sequences, and the ordering and quoting rules."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Filename-Expansion
  - https://www.gnu.org/software/bash/manual/bash.html#Brace-Expansion
  - https://www.gnu.org/software/bash/manual/bash.html#The-Shopt-Builtin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Globbing, extglob and brace expansion — generating filenames and words

**Goal:** match exactly the files you mean (including dotfiles and recursive trees), handle
the no-match case deliberately, and generate argument lists with braces.

## 1. Basic globs
```bash
ls *.log            # any chars (not leading dot, not /)
ls ?.txt            # one char
ls [abc]*.conf  [!0-9]* [[:upper:]]*     # sets, negation, POSIX classes
ls /etc/*/*.conf    # * does not cross /; use globstar for depth
```
- Globs are expanded by the shell **before** the command runs; `ls *.log` never sees `*.log`.
- A glob with no match stays **literal** by default → `rm *.tmp` tries to remove a file
  named `*.tmp` (and errors). See nullglob/failglob.
- Order is locale-sorted; `LC_COLLATE=C` for ASCII order.

## 2. shopt switches
```bash
shopt -s globstar     # ** matches recursively:  for f in src/**/*.py
shopt -s nullglob     # no match → expands to nothing (loops run 0 times) — standard in scripts
shopt -s failglob     # no match → error; good for interactive safety
shopt -s dotglob      # * includes dotfiles (never . and ..)
shopt -s nocaseglob   # case-insensitive matching
shopt -s extglob      # extended patterns below
shopt -u ...          # turn off; check with: shopt globstar
```
`nullglob` has a trap: `ls *.foo` with no match becomes `ls` of the cwd. Combine with
explicit existence checks in interactive use; in scripts prefer loops.

## 3. extglob
```bash
shopt -s extglob
rm !(*.conf|*.bak)              # everything except
ls +(a|b)*.log                  # one or more of
ls ?(pre-)file.txt              # zero or one
ls *(x)                         # zero or more
ls @(jpg|png)                   # exactly one
cp -- !(.git) /dest/            # with dotglob to include dotfiles
```
Same patterns work in `case`, `[[ == ]]` and `${var//pat/}`; `shopt -s extglob` must be
set **before** the line is parsed (in a script, put it before functions that use it).

## 4. Brace expansion (not a glob — no filesystem involved)
```bash
mkdir -p /srv/app/{bin,conf,log}
cp file.conf{,.bak}               # file.conf file.conf.bak
echo {1..10} {a..e} {01..10} {0..100..5}
echo img{001..100}.png
echo {a,b}{1,2}                   # a1 a2 b1 b2 (cartesian)
```
- Happens **first**, before variable expansion: `{1..$n}` does not work — use `seq`/C-for.
- Must contain a comma or `..` and no spaces; quoted braces are literal.
- Disable with `set +B` (`set +o braceexpand`).

## 5. Quoting and safety
```bash
f="my *.txt"; ls "$f"          # quoted: no glob on the value
ls -- *.txt                    # -- protects against files named -r
for f in ./*; do ...; done     # leading ./ prevents filenames starting with -
printf '%s\n' *                # list safely, one per line, spaces intact
```
`find` vs globs: globs are fine for one directory or `**`; anything by time/size/type
belongs to `find`.

## Failure modes
- `rm: cannot remove '*.tmp'`: no match, literal passed — nullglob or test first.
- `**` acts like `*`: globstar off (it is off by default; shell options are not inherited by scripts, so set it in the script). Since bash 4.3 `**` does not traverse symlinks to directories.
- Dotfiles skipped by `cp -r * dest`: dotglob, or `cp -r . dest`.
- `[a-z]` matches uppercase: only on bash < 5.0 (or after `shopt -u globasciiranges`) in a locale with dictionary collation; `globasciiranges` is on by default since bash 5.0 (bash NEWS; `[a-z]*` skipped `Zed` on 5.2) — use `[[:lower:]]` to be explicit.
- Brace expansion produced literal `{a,b}`: inside quotes, or `set +B`, or non-bash `sh`.

## Verify
- [ ] `shopt -s nullglob; echo *.nope` prints an empty line; `shopt -u nullglob` prints `*.nope`.
- [ ] `echo {01..03}{a,b}` prints six words.
