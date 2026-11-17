---
id: computing-software.systems-network-administration.bash.shell-dates-and-time-arithmetic
name: shell-dates-and-time-arithmetic
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-date-command, date-arithmetic, epoch-time, gnu-vs-bsd-date]
level: practitioner
status: draft
description: "Format, parse and compute with dates in shell using GNU date, BSD date and epoch seconds."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dates in shell

- Format: `date +%Y-%m-%d`, ISO-8601 UTC `date -u +%Y-%m-%dT%H:%M:%SZ`, epoch `date +%s`. Bash 4.2+ `printf '%(%F %T)T\n' -1` or an epoch argument formats without forking.
- GNU date parses free text: `date -d '2025-03-01 12:00' +%s`, `date -d '3 days ago'`, `date -d @1700000000`, `date -d 'last friday'`. BSD/macOS uses `date -j -f '%Y-%m-%d' '2025-03-01' +%s` and `date -v+3d`. Install GNU coreutils (`gdate`) on macOS for portable scripts.
- Do arithmetic in epoch seconds with `$(( ))`, not on formatted strings; convert at the edges. Days between: `(( (end - start) / 86400 ))` (ignores DST unless both in UTC).
- Time zones: `TZ=America/New_York date`; set `TZ` for the single command. Store and log in UTC.
- Elapsed time: `SECONDS` (bash), `$EPOCHREALTIME` (bash 5) for sub-second, `time` keyword; for monotonic timing use `/proc/uptime`, since wall-clock can jump.
- `date +%F -d "$input" >/dev/null 2>&1` validates a date (GNU).
