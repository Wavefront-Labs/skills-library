---
id: computing-software.systems-network-administration.bash.shell-cron-and-non-interactive-environment
name: shell-cron-and-non-interactive-environment
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-cron-environment, non-interactive-shell, minimal-path, systemd-timers]
level: practitioner
status: draft
description: "Make scripts run reliably under cron, systemd and CI with explicit PATH, HOME, locale and absolute paths."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cron and non-interactive environments

- cron runs commands with a minimal environment (`PATH=/usr/bin:/bin`, `SHELL=/bin/sh`, no profile files). Set `PATH`, `LANG`/`LC_ALL=C` (or a UTF-8 locale), `HOME` and `TZ` inside the script, and call tools with full paths where PATH differs.
- `SHELL=/bin/bash` can be set in the crontab; otherwise `/bin/sh` is dash on Debian/Ubuntu, so bashisms fail with errors only visible in mail/logs.
- `%` is special in crontab command lines (newline): escape as `\%` (this bites `date +%F`).
- Use absolute paths; `cd "$(dirname "$0")" || exit 1` at the top (see script-directory skill).
- Capture failures: redirect to a log, set `MAILTO`, or use `systemd` timers (journald logs, `Persistent=true`, no overlapping runs by default, `OnCalendar=` syntax verified with `systemd-analyze calendar`).
- Prevent overlap with `flock`. Test the exact environment: `env -i HOME="$HOME" PATH=/usr/bin:/bin /bin/sh -c '/path/to/script'`.
- Bash startup files are not read by non-interactive shells unless `BASH_ENV` is set.
