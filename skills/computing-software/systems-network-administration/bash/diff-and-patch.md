---
id: computing-software.systems-network-administration.bash.diff-and-patch
name: diff-and-patch
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, diff-patch, unified-diff, diff, patch, colordiff, config-drift, hunk]
level: practitioner
status: verified
description: "Compare files and trees with diff -u/-r, create and apply patches with patch -p, dry-run and reverse, handle rejects and fuzz, and spot config drift between hosts."
sources:
  - https://www.gnu.org/software/diffutils/manual/diffutils.html
  - https://man7.org/linux/man-pages/man1/patch.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# diff and patch

## Compare
```bash
diff -u old.conf new.conf                       # unified format (3 lines context); exit 0 same, 1 differ, 2 trouble
diff -u -w a b ; diff -u -B a b                  # ignore whitespace / blank lines
diff -ruN orig/ modified/ > change.patch         # recursive, treat absent files as empty (-N)
diff -q -r dir1 dir2                             # just which files differ
diff <(ssh web1 cat /etc/nginx/nginx.conf) <(ssh web2 cat /etc/nginx/nginx.conf)   # drift between hosts
diff --color=auto -u a b ; sdiff -s a b ; vimdiff a b
cmp file1.bin file2.bin                          # binary
```
Reading a hunk: `@@ -12,7 +12,8 @@` = old lines start 12 count 7 → new start 12 count 8; `-` removed, `+` added.

## Apply
```bash
patch -p1 --dry-run < change.patch     # -pN strips N leading path components (a/ b/ from git → -p1)
patch -p1 < change.patch
patch -R -p1 < change.patch             # reverse/undo
patch -p1 -b < change.patch             # keep .orig backups
patch /etc/app.conf < single-file.diff  # target given explicitly
```
`git apply --check change.patch` / `git apply` also work outside a repo (tested with git 2.46; default `-p1`).

## Rejects and fuzz
- `Hunk #2 succeeded at 140 (offset 12 lines)` — fine.
- `with fuzz 2` — context partly mismatched; review the result.
- `Hunk #3 FAILED ... saving rejects to file x.rej` — apply `.rej` by hand, delete `.rej` and `.orig` after.
- "Reversed (or previously applied) patch detected! Assume -R? [n]" — it's already applied; answer `n` (a hunk is then saved to `.rej`; tested).

## Gotchas
- CRLF line endings make every line differ: `diff --strip-trailing-cr`, or `dos2unix`.
- Patches from email/web may lose tabs → hunks fail; fetch raw.

## Verify
- [ ] `patch --dry-run` clean before applying; after applying, `diff -u` against the expected file is empty.
