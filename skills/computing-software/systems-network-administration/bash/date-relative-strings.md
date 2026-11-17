---
id: computing-software.systems-network-administration.bash.date-relative-strings
name: date-relative-strings
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, date-relative-strings, date-d, shell-scripting]
level: practitioner
status: draft
description: "Compute dates with GNU date -d relative strings like yesterday, last friday and 3 days ago, and BSD equivalents."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Relative dates with date -d
**Goal:** date arithmetic without loops.
```bash
date -d yesterday +%F
date -d '3 days ago' +%F
date -d 'next friday' +%F
date -d 'last month' +%Y-%m
date -d '2026-11-02 +1 week' +%F
date -d '2026-03-31 -1 month' +%F      # month math clamps oddly: check results
echo $(( ( $(date -d 2026-12-25 +%s) - $(date +%s) ) / 86400 ))   # days until
# BSD/macOS: date -v-3d +%F ; date -v+1w -j -f %F 2026-11-02 +%F
```
- Convert to epoch (`+%s`) for any arithmetic, then back.
- DST: adding `24 hours` differs from `1 day` across a transition; use noon (`12:00`) to dodge it.
- Month-end jumps (`Jan 31 +1 month`) roll into the next month.
- Parse failures return non-zero: check `$?`.
- Self-check: `date -d '1 day ago' +%F` is yesterday.
