---
id: computing-software.systems-network-administration.bash.bash-loops-for-while-read
name: bash-loops-for-while-read
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, loops, for-loop, while-read, until-loop, c-style-for, read-r, ifs, line-by-line, subshell-pipe-loop, break-continue, seq, brace-range, shell-scripting, rhcsa, sysadmin]
level: practitioner
status: verified
description: "Write bash loops that survive real data: for over globs/arrays/ranges, while IFS= read -r line, C-style for, reading files without a subshell, break/continue levels, and the stdin-stealing ssh trap."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Looping-Constructs
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins
  - https://mywiki.wooledge.org/BashFAQ/001
  - https://manpages.debian.org/unstable/openssh-client/ssh.1.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loops — for, while read, and the three mistakes everyone makes once

**Goal:** iterate over files, lines and ranges without word-splitting bugs, lost variables
in subshells, or a loop that silently ran once.

## 1. for — over words, globs, arrays, ranges
```bash
for f in /var/log/*.log; do [[ -e $f ]] || continue; gzip "$f"; done   # guard: unmatched glob stays literal
for host in "${hosts[@]}"; do ssh "$host" uptime; done
for i in {1..10}; do ...; done            # brace range, fixed at parse time
for i in $(seq 1 "$n"); do ...; done      # variable bound (or C-style below)
for ((i=0; i<n; i++)); do echo "$i"; done
for ((;;)); do ...; done                  # infinite
```
- **Never** `for f in $(ls)` or `for l in $(cat file)` — splits on whitespace, expands globs.
- `shopt -s nullglob` makes an unmatched glob expand to nothing (loop runs zero times);
  `failglob` makes it an error. Pick one for scripts.
- `for f in *` skips dotfiles unless `shopt -s dotglob`.

## 2. while read — the line loop
```bash
while IFS= read -r line; do
    printf '%s\n' "$line"
done < file.txt
```
- `IFS=` keeps leading/trailing whitespace; `-r` stops backslash interpretation.
- Last line without a trailing newline is dropped unless: `while IFS= read -r l || [[ -n $l ]]`.
- Fields: `while IFS=: read -r user _ uid gid _ home shell; do ...; done < /etc/passwd`.
- NUL-delimited (filenames): `while IFS= read -r -d '' f; do ...; done < <(find . -print0)`.
- Interactive/progress: `read -t 5` timeout, `read -n 1` single char, `read -s` silent.

## 3. Pipes create subshells — variables vanish
```bash
count=0
cat f | while read -r l; do ((count++)); done; echo "$count"   # prints 0!
while read -r l; do ((count++)); done < f                      # redirect instead: works
while read -r l; do ((count++)); done < <(cmd)                 # process substitution: works
shopt -s lastpipe   # bash 4.2+, non-interactive: last pipeline stage runs in current shell
```

## 4. Commands inside the loop that eat stdin
```bash
while read -r host; do ssh "$host" uptime; done < hosts     # runs ONCE: ssh reads stdin (any stdin reader does; tested with cat)
while read -r host; do ssh -n "$host" uptime; done < hosts  # -n redirects stdin from /dev/null (ssh man page); or </dev/null
while read -r -u 3 host; do ssh "$host" uptime; done 3< hosts   # dedicated fd: robust
```
Same trap with `ffmpeg`, `mysql`, `apt` — anything reading stdin. Use `-u 3`/`3<` when in doubt.

## 5. Control flow
```bash
for ...; do for ...; do [[ $x == skip ]] && continue 2; [[ $x == stop ]] && break 2; done; done
until ping -c1 -W1 "$h" &>/dev/null; do sleep 2; done     # until: loop while FALSE
while :; do ...; done                                      # : is true, no fork
```
`break N`/`continue N` apply to N enclosing loops. Loops return the status of the last
command; `set -e` does not fire on a failing command used as the loop condition.

## 6. Performance notes
- Spawning a process per line (`sed`, `cut`) in a 100k-line loop is slow; use parameter
  expansion (`${l%%:*}`) or hand the whole file to awk.
- `mapfile -t lines < file` then `for l in "${lines[@]}"` when you need random access or a count.
- `read` is fine for thousands of lines; for millions use awk/`xargs -P`.

## Failure modes
- Loop runs once over a file with many lines: stdin consumed (ssh/mysql) — section 4.
- Filenames with spaces split into pieces: `$(ls)`/unquoted `$f`.
- Variables empty after the loop: pipe subshell — section 3.
- `{1..$n}` prints literally: brace expansion precedes variable expansion; use `seq`/C-for.
- Backslashes disappear / `\n` interpreted: missing `read -r`.

## Verify
- [ ] Feed a test file whose last line lacks `\n` and whose lines have leading spaces and backslashes; the loop reproduces it byte-for-byte (`printf '%s\n'` + `cmp`).
- [ ] A loop around `ssh` processes every host in the list.
