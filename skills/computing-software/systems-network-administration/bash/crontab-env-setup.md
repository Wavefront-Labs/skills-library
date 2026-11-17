---
id: computing-software.systems-network-administration.bash.crontab-env-setup
name: crontab-env-setup
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, crontab-env-setup, crontab-percent, shell-scripting]
level: practitioner
status: docs-checked
description: "Set PATH, SHELL, MAILTO and logging in crontab so shell scripts run reliably under cron's minimal environment."
sources:
  - https://man7.org/linux/man-pages/man5/crontab.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting PATH and SHELL in crontab
**Goal:** cron jobs that behave like your terminal.
```
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=ops@example.com
# m h dom mon dow  command
15 2 * * *  /opt/scripts/backup.sh >>/var/log/backup.log 2>&1
*/5 * * * * flock -n /run/poll.lock /opt/scripts/poll.sh
0 3 * * *   cd /opt/app && ./run.sh
```
- cron sets `SHELL` to `/bin/sh` and sets `LOGNAME` and `HOME` from the owner's `/etc/passwd` line; a crontab can override `HOME` and `SHELL` but not `LOGNAME`. The man page lists no other variables, so set `PATH` yourself or use absolute paths.
- The command runs up to a newline or an unescaped `%`: each unescaped `%` becomes a newline and everything after the first one is sent to the command as standard input. Escape it as `\%` (as in `date +\%F`).
- `MAILTO` set and non-empty mails output to that address; `MAILTO=""` sends no mail; unset sends it to the crontab owner.
- Edit with `crontab -e`. Jobs in `/etc/cron.d` and `/etc/crontab` are system jobs and need a username field before the command.
- Every crontab entry must end in a newline.
- Self-check: temporarily add `env > /tmp/cronenv` and compare it to the interactive `env`.

## Checked
2026-11-08. Confirmed against the crontab(5) man page: variables set by cron and which can be overridden, `MAILTO` behaviour, `%` handling and escape, `crontab -e`, the cron.d username field and the trailing newline rule. Removed the claims about a default PATH value, that cron does not read `.bashrc`/`.profile`, and `crontab -l`, which the page does not state.
Method: documentation only; no commands were run.
