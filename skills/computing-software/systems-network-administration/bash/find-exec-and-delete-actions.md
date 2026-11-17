---
id: computing-software.systems-network-administration.bash.find-exec-and-delete-actions
name: find-exec-and-delete-actions
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, find, find-exec, find-delete, exec-plus, find-ok, find-print0, xargs, depth, prune, file-management, lfcs, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Act on find results safely: -exec {} \\; vs -exec {} +, -delete ordering rules, -ok for confirmation, -print0 | xargs -0, -prune, and dry-running before destructive runs."
sources:
  - https://man7.org/linux/man-pages/man1/find.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# find -exec and -delete — acting on matches without a catastrophe

**Goal:** run commands or deletions on exactly the files `find` matched, efficiently, and
with the expression ordered so the action applies only after all the tests.

## 1. Always dry-run first
```bash
find /var/tmp -type f -mtime +30 -print          # look at the list
find /var/tmp -type f -mtime +30 -delete         # then act
```
`-print` is implied only when no action is given; once you add `-exec`/`-delete`, nothing is
printed unless you add `-print` yourself.

## 2. -exec forms
```bash
find . -name '*.log' -exec gzip {} \;            # one process per file (slow, but simple)
find . -name '*.log' -exec gzip {} +             # batches many files per process (like xargs)
find . -type f -exec grep -l 'TODO' {} +         # fast recursive grep via find's filters
find . -name '*.bak' -ok rm {} \;                # prompts y/n per file
find . -type d -exec sh -c 'cd "$1" && make clean' sh {} \;   # need shell features? wrap in sh -c with $1
```
- `{} +` must be the last thing before `+`; `{}` can appear only once in that form.
- `\;` must be escaped from the shell; `+` need not.
- `-execdir` runs the command from the file's directory with `./name` — safer for
  untrusted trees (no path-based tricks) and required when the command cannot take long paths.
- Exit status of the command feeds the expression: `find . -exec test -w {} \; -print`
  prints only writable files.

## 3. -delete rules
- `-delete` implies `-depth` (children before parents) so directories are emptied first.
  Because of `-depth`, `-prune` **does not work** in the same command (find warns: "-prune does nothing when -depth is in effect") — delete with
  `-exec rm` or `-print0 | xargs -0 rm` if you need pruning.
- Put `-delete` **last**. `find . -delete -name '*.tmp'` deletes everything (the action
  runs before the test, and `-delete` is also true).
- It refuses non-empty directories (`Directory not empty`) — add `-type f` or accept.
- `find -delete` cannot cross into another filesystem by accident if you add `-xdev`.

## 4. Pipeline form with NUL separators
```bash
find /srv -type f -name '*.jpg' -print0 | xargs -0 -P4 -n50 jpegoptim
find . -newer ref -print0 | while IFS= read -r -d '' f; do printf '%s\n' "$f"; done
```
Filenames may contain newlines and spaces; `-print0`/`-0`/`read -d ''` is the only safe
channel. Plain `find | xargs` breaks on `My Photos.jpg`.

## 5. Scoping and pruning
```bash
find / -xdev -size +500M                         # stay on one filesystem (skip /proc, NFS)
find . -path ./node_modules -prune -o -name '*.js' -print   # skip a subtree; -print is REQUIRED after -o
find /var/log -maxdepth 1 -type f               # no recursion into subdirs
find . -mindepth 1 -maxdepth 1 -type d           # immediate children only
```
Without the explicit `-print` after `-o`, the pruned directory itself is printed (the
implicit print wraps the whole expression).

## Failure modes
- "find: missing argument to -exec": forgot `\;` or `+`.
- Command ran on nothing: tests after the action; or `-name` pattern unquoted and expanded
  by the shell against the current directory.
- `-exec rm -rf {}` on a path containing a symlink to `/`: find does not follow symlinks by
  default (good) — never add `-L` to a deleting find.
- Deleting too much with `-mtime +N`: `+30` means more than 30 *full* days (31+); `-mtime 30`
  is exactly 30.

## Verify
- [ ] The `-print` dry run and the action run list the same count (`| wc -l` vs `-exec echo`).
- [ ] After `-delete`, `find <same tests>` returns nothing, and parent directories still exist.
