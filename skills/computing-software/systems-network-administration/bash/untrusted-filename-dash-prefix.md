---
id: computing-software.systems-network-administration.bash.untrusted-filename-dash-prefix
name: untrusted-filename-dash-prefix
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, untrusted-filename-dash-prefix, option-injection, shell-scripting]
level: practitioner
status: draft
description: "Protect commands from filenames beginning with a dash or containing newlines by using -- and ./ prefixes in shell scripts."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filenames starting with a dash
**Goal:** untrusted names must not become options.
```bash
rm -- "$file"                # -- ends option parsing
cp -- "$src" "$dst"
for f in ./*; do ls -l -- "$f"; done      # ./ prefix makes names path-like
grep -e "$pattern" -- "$file"             # pattern starting with - needs -e
find . -name "$name" -print0
```
- A file named `-rf` or `--no-preserve-root` globbed by `rm *` is read as flags; `./*` or `-- *` prevents it.
- `--` support is near-universal but not guaranteed for every tool (e.g. `echo`, `test`); check or avoid.
- Newlines in names break line-based loops: use `-print0` and `read -d ''`.
- Self-check: `touch -- -x; rm -- -x` works; `rm -x` errors.
