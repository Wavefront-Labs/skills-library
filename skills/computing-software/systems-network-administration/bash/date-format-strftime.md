---
id: computing-software.systems-network-administration.bash.date-format-strftime
name: date-format-strftime
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, date-format-strftime, strftime, shell-scripting]
level: practitioner
status: draft
description: "Format timestamps with date +FORMAT in shell scripts: ISO 8601, epoch seconds, filenames, timezones and UTC."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# date format strings
**Goal:** correct, sortable time strings.
```bash
date +%F                       # 2026-11-02
date +%Y%m%dT%H%M%S%z          # 20261102T143000+0000
date -u +%Y-%m-%dT%H:%M:%SZ    # UTC ISO 8601
date +%s                       # epoch seconds
date -d @1700000000 +%F        # GNU: epoch to date   (BSD: date -r 1700000000)
TZ=Asia/Tokyo date +%R
date +%Y-%m-%d_%H-%M-%S        # filename safe: no colons
printf '%(%F %T)T\n' -1        # bash 4.2: no fork
```
- Use UTC (`-u`) for logs and stored data; local time for display.
- `%e` pads with space, `%d` with zero; `%j` day of year; `%G-W%V` ISO week.
- GNU and BSD flags differ (`-d` vs `-v/-j -f`).
- Self-check: `date -u +%FT%TZ` matches the clock.
