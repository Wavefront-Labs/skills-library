---
id: computing-software.systems-network-administration.bash.grep-recursive-and-context-search
name: grep-recursive-and-context-search
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, grep, grep-recursive, grep-context, grep-r, include, exclude-dir, grep-l, grep-c, binary-files, ripgrep, text-processing, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Search trees with grep -r: include/exclude globs, -A/-B/-C context, -l/-L/-c summaries, binary and symlink handling, and when ripgrep is the better tool."
sources:
  - https://www.gnu.org/software/grep/manual/grep.html
  - https://man7.org/linux/man-pages/man1/grep.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursive and context grep — find the needle without drowning in the haystack

**Goal:** search a whole tree for a pattern, scope it to the files that matter, and get
output you can read (context lines, file lists, counts) instead of a wall of matches.

## 1. Recursion and scoping
```bash
grep -rn 'listen_addresses' /etc/postgresql/        # -r recurse, -n line numbers
grep -rnI --include='*.conf' --exclude-dir={.git,node_modules} 'Listen' /etc/
grep -rl 'TODO' src/            # -l: file names only (stops at first match per file — fast)
grep -rL 'Copyright' src/       # -L: files WITHOUT a match
grep -rc 'ERROR' /var/log/app/  # -c: count per file (includes 0s; filter with | grep -v ':0$')
```
- `-r` does not follow symlinks except those on the command line; `-R` follows all.
  On `/etc` with `-R` you can loop through `/etc/alternatives` — prefer `-r`.
- `-I` skips binary files; `--binary-files=text` (or `-a`) forces matching inside them.
  "Binary file X matches" lines mean grep saw NUL bytes — often a log with a NUL from a crash.
- `--include`/`--exclude` match the **basename** only; quote the glob so the shell does
  not expand it. `--exclude-dir` matches directory basenames at any depth.

## 2. Context
```bash
grep -n -B2 -A5 'Traceback' app.log   # 2 before, 5 after
grep -C3 'segfault' /var/log/kern.log  # 3 each side; groups separated by "--"
grep --no-group-separator -A1 '^Package:' Packages
```
With `-r`, context lines are prefixed `file-NN-` (dash) and matches `file:NN:` (colon) —
useful for scripts to tell them apart.

## 3. Multiple patterns and fixed strings
```bash
grep -rE 'error|fatal' logs/            # ERE alternation
grep -rF -f bad-ips.txt /var/log/nginx/ # -F: literal strings from a file, no regex escaping; fast
grep -rw 'root' /etc/                   # whole word (-w); -x whole line
grep -rin 'warn' --color=always app.log | less -R
```
`-F -f list` is the right way to match thousands of literal strings; a regex alternation
of the same list is orders of magnitude slower.

## 4. Output control for pipelines
```bash
grep -rHn pattern file        # -H forces the filename even for one file; -h hides it
grep -o -E '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' access.log | sort | uniq -c | sort -rn | head
grep -m1 'Started' boot.log   # stop after first match
grep -q pattern file && echo found   # -q: exit status only (0 match, 1 none, 2 error)
grep -rZl pattern . | xargs -0 sed -i 's/old/new/g'   # -Z/-null: NUL-separated names for xargs -0
```

## 5. When to switch to ripgrep
`rg` respects `.gitignore`, skips binaries and hidden files by default, is multithreaded
and much faster on big trees. `rg -n -g '*.conf' Listen /etc` ≈ the include form above;
`rg -uu` to stop ignoring hidden/ignored files. For scripts that must run everywhere
(minimal containers, rescue shells), stay with GNU grep.

## Failure modes
- `grep -r pattern` with no path searches the working directory (grep(1); tested on 3.0), not stdin; pass `-` explicitly to read stdin. Very old greps (2.5-2.10) warned "recursive search of stdin" (gated: unconfirmed, source is paywalled or blocked).
- Nothing matches a pattern with `+` or `|`: BRE is the default — use `-E` or escape.
- Huge slowdown on `/`: you hit `/proc` or `/sys`; `--exclude-dir={proc,sys,dev,run}` or
  search a narrower root.
- Locale: `LC_CTYPE` governs character classes and range expressions (grep(1)); `LC_ALL=C` restores traditional byte behaviour, so pick deliberately.

## Verify
- [ ] `grep -rc` totals agree with `grep -r | wc -l` for the same pattern and scope.
- [ ] `--include` glob actually limited the set: `grep -rl --include='*.conf' . | grep -v '\.conf$'` is empty.
