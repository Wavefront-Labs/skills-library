---
id: computing-software.systems-network-administration.bash.find-regex-maxdepth
name: find-regex-maxdepth
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, find-regex-maxdepth, find-prune, shell-scripting]
level: practitioner
status: draft
description: "Limit find depth and match whole paths with -maxdepth, -mindepth and -regex, and mind option order and regex types."
sources:
  - https://www.gnu.org/software/findutils/manual/html_mono/find.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# find -regex and -maxdepth
**Goal:** precise, efficient file searches.
```bash
find . -maxdepth 1 -type f                 # current dir only
find . -mindepth 2 -maxdepth 3 -name '*.conf'
find . -regextype posix-extended -regex '.*/[0-9]{4}-[0-9]{2}\.log'
find . -path './node_modules' -prune -o -type f -name '*.js' -print
find . -type f \( -name '*.jpg' -o -name '*.png' \)
find / -xdev -type f -size +100M 2>/dev/null
```
- `-regex` matches the WHOLE path (including `./`), not just the name.
- Put `-maxdepth`/`-mindepth` first or GNU find warns; BSD find uses `-depth N` differently (`-maxdepth` supported on modern BSD).
- `-prune` needs `-o ... -print` so pruned items are not printed.
- Parenthesise `-o` groups; `-a` binds tighter than `-o`.
- Self-check: `find . -maxdepth 1 | wc -l` counts only top-level entries.
