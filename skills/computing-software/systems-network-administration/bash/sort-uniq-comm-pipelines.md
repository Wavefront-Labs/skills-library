---
id: computing-software.systems-network-administration.bash.sort-uniq-comm-pipelines
name: sort-uniq-comm-pipelines
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, sort, uniq, comm, join, sort-uniq, sort-k, sort-by-column, numeric-sort, version-sort, uniq-c, set-difference, deduplicate, lc-all, text-processing, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Sort by column with -k/-t, numeric/human/version sorts, uniq -c/-d/-u counting, and comm/join set operations — with the locale and whitespace traps that silently corrupt results."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/uniq-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/comm-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sort / uniq / comm pipelines — the Unix group-by and set algebra

**Goal:** rank, count, deduplicate and diff lists correctly, which mostly means knowing
that `uniq` needs sorted input and `sort -k` keys run to end of line unless told otherwise.

## 1. Sorting by a column
```bash
sort -t: -k3,3n /etc/passwd                 # by UID, numeric; -k3,3 = field 3 only
sort -k2,2 -k1,1n file                      # secondary key
du -sh /* 2>/dev/null | sort -h             # human sizes (K/M/G)
ls /lib/modules | sort -V                   # version sort: 5.10.9 < 5.10.10
sort -rn -k5 | head                         # descending by field 5 (-rn applies to all keys)
sort -u -t, -k1,1 file.csv                  # unique by first field; -u outputs only the first of lines with equal keys (sort(1))
```
- `-k3` alone means "from field 3 to end of line"; write `-k3,3`.
- Field separator defaults to the transition from non-blank to blank, so leading spaces
  belong to the field. `-t` makes it exact. `-b` ignores leading blanks.
- `-s` (stable) plus a key keeps input order for ties; without it ties are compared whole-line.

## 2. Counting with uniq
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head      # top talkers
sort file | uniq -d          # only duplicated lines (once each)
sort file | uniq -u          # only lines that appear exactly once
uniq -c -w 10 file           # compare only first 10 chars
sort f | uniq -ci            # case-insensitive
```
`uniq` only collapses **adjacent** duplicates — always `sort` first unless the input is
already grouped. `sort | uniq` == `sort -u` but `uniq -c` has no sort equivalent.

## 3. Set operations with comm and join
```bash
comm -23 <(sort a) <(sort b)     # in a, not in b     (columns: 1=only a, 2=only b, 3=both)
comm -13 <(sort a) <(sort b)     # in b, not in a
comm -12 <(sort a) <(sort b)     # intersection
join -t, -1 1 -2 1 <(sort -t, -k1,1 users.csv) <(sort -t, -k1,1 groups.csv)   # inner join on col 1
join -a1 -e MISSING -o 0,1.2,2.2 ...   # left join with filler
```
`comm` and `join` require inputs sorted with the **same** `sort` invocation (same locale,
same key). Mismatch gives a "not in sorted order" error (`comm: input is not in sorted order` on coreutils 8.32; `join` reports the file) or silently wrong output.

## 4. Locale: the silent corrupter
```bash
LC_ALL=C sort file      # byte order: uppercase before lowercase, punctuation ordered predictably; fastest
```
Locale collation can differ from byte order (`printf 'B
a
' | LC_ALL=C sort` gives `B` then `a`; the exact ordering of other locales such as `en_US.UTF-8` depends on the system's locale data, not tested here), so `comm`/`join` inputs sorted
under different locales can mismatch and `sort -c` can report unsorted. Pin `LC_ALL=C` in scripts
whenever the output feeds another tool.

## 5. Scale
- `sort -S 2G --parallel=4` for multi-GB files; it spills to `$TMPDIR` — point `-T` at a disk
  with space.
- `sort -m` merges already-sorted files without re-sorting.
- `--debug` underlines the exact bytes used as key — the fastest way to debug a wrong `-k`.

## Failure modes
- "Numbers sort wrong (10 before 9)": missing `-n`; mixed units need `-h`; versions need `-V`.
- `uniq -c` counts look split (same value counted twice): input not sorted, or trailing
  whitespace/CR differences — `sed 's/[[:space:]]*$//'` or `dos2unix` first.
- `join` prints nothing: keys not sorted identically, or default FS (whitespace) vs `-t,`.

## Verify
- [ ] `sort -c` (or `sort -t, -k1,1 -c`) on the sorted input exits 0.
- [ ] `comm` column counts add up: `|only-a| + |both| == wc -l a` (after `sort -u`).
