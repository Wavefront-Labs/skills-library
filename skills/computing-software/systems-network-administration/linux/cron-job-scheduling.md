---
id: computing-software.systems-network-administration.linux.cron-job-scheduling
name: cron-job-scheduling
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cron, crontab, anacron, flock, run-parts, mailto, cron-env, cron-path, scheduling, overlapping-jobs, timezone, sysadmin, cron-d, crontab-syntax]
level: practitioner
status: verified
description: "Write correct crontab entries and avoid cron's classic failure modes: minimal PATH/env, silent mail, overlapping runs, and timezone surprises."
sources:
  - https://github.com/cronie-crond/cronie/blob/master/man/crontab.5
  - https://github.com/cronie-crond/cronie/blob/master/man/cron.8
  - https://github.com/cronie-crond/cronie/blob/master/man/anacron.8
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
  - https://man7.org/linux/man-pages/man1/flock.1.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# cron job scheduling — still the right tool for simple, user-level jobs

**Goal:** write crontab entries that actually run the way they do
interactively, catch failures instead of letting them vanish into an unread
mailbox, and know when cron is genuinely the right call versus when a
systemd timer (see
`computing-software.systems-network-administration.linux.systemd-timers-and-advanced-units`)
is worth the extra setup.

## 1. Syntax, and the field most people get wrong
```
# min hour dom month dow   command
30   2    *   *     *      /opt/app/backup.sh
0    */4  *   *     *      /opt/app/sync.sh        # every 4 hours
0    9    *   *     1-5    /opt/app/report.sh       # weekdays only
```
`dom` (day of month) and `dow` (day of week) are **OR'd**, not AND'd, when
both are restricted from `*` — `0 0 1,15 * 5` runs on the 1st AND 15th of
the month, AND every Friday, not only Fridays that happen to fall on those
dates. This trips people writing "run on the 1st, only if it's a weekday"
logic, which cron's syntax can't express directly — that needs a wrapper
script checking `date +%u` itself.
```bash
crontab -l                     # current user's crontab
crontab -e                     # edit it (uses $EDITOR)
sudo crontab -u otheruser -l    # another user's
```
System-wide jobs also live in `/etc/cron.d/*` and `/etc/crontab` (both have an extra
user name field after the time fields). In cronie, `/etc/crontab` holds no jobs by default (only SHELL, PATH, MAILTO and comments; the hourly job is in `/etc/cron.d/0hourly`) and the
daily/weekly/monthly jobs run through anacron (`/etc/anacrontab`). Test a crontab's syntax with `crontab -T`.
The commands below describe cronie (the cron(8)/crontab(5) pages from cronie-crond/cronie); other cron implementations differ.

## 2. The environment is NOT your shell's environment
```
# in a crontab:
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=ops@example.com
30 2 * * * /opt/app/backup.sh
```
cron sets `SHELL` to /bin/sh and `LOGNAME`/`HOME` from the crontab owner's passwd entry
(`HOME` and `SHELL` can be overridden in the crontab). It does not run your interactive shell
profile, so aliases and variables from it are absent: "works by hand but not from cron" is usually
this. Set needed variables explicitly in the crontab, or use absolute paths inside the script.
Environment lines are `name = value`, and comments are not allowed on the same line as a command
or a variable setting (`crontab -T` does not flag a comment after a variable setting).

## 3. Output and failure visibility
```
MAILTO=ops@example.com
30 2 * * * /opt/app/backup.sh > /var/log/backup.log 2>&1 || echo "backup failed" | mail -s "backup FAILED" ops@example.com
```
By default cron mails a job's output to the crontab owner (or to `MAILTO` if set and non-empty;
`MAILTO=""` sends no mail). Do not rely on cron mail as the only failure signal: redirect output to
a log file and add explicit alerting in the job itself.

## 4. Overlapping runs — cron does not prevent them
```
* * * * * flock -n /tmp/myjob.lock /opt/app/myjob.sh
```
Cron fires a new instance on schedule regardless of whether the previous
run finished — a job that occasionally takes longer than its interval
silently stacks up concurrent runs until something breaks (DB lock
contention, duplicate processing, disk fills from parallel writes).
`flock -n` (`--nonblock`) fails instead of waiting when the lock is held (exit status 1 by default, `-E` changes it), so the
second invocation does not run. With a systemd timer, if the unit to activate is already active when the
timer elapses it is left running and not restarted (systemd.timer(5)).

## 5. Anacron — catching up missed runs on machines that aren't always on
```
# /etc/anacrontab
1       5       cron.daily      run-parts /etc/cron.daily
```
Anacron does not assume the machine runs continuously: for each job it checks whether the job ran
in the last N days (the period) and, if not, runs it after the delay in minutes. Plain cron has no
catch-up for a missed time. A systemd timer with `Persistent=true` is the systemd alternative.

## 6. When to pick cron vs a systemd timer
Cron suits simple user-level jobs and systems without systemd. Systemd timers give dependency ordering on
other units, no restart of an already-active unit, journal logging, `Persistent=` catch-up and per-service
resource limits. Mixed estates can keep both.

## Gotchas
- Cron's time is the daemon's local time; `CRON_TZ=<zone>` in a crontab sets the time zone for that cron table
  (entries are written in that zone; the log still uses the daemon's local time zone).
- `%` in a crontab command is turned into a newline unless escaped `\%`, and data after the first `%` goes to the command's standard input; a command
  using `date +%Y%m%d` directly in the crontab line breaks unless escaped.
- `*/N` steps apply within a field: `*/35` in the minute field runs at minutes 0 and 35 every hour, not every 35 minutes.
- Every crontab entry must end in a newline.

## Verify
- [ ] The crontab line's schedule matches intent (watch the dom/dow OR rule); `crontab -T` accepts the file.
- [ ] Output is captured to a log file and failure triggers something beyond unread local mail.
- [ ] A job that can run long has an overlap guard (`flock` or equivalent) tested by deliberately running two instances at once.
- [ ] The command works with only the variables set in the crontab (SHELL, LOGNAME, HOME and your own).

## Checked

Checked against the cronie man pages cron(8), crontab(1), crontab(5), anacron(8) and anacrontab(5) (cronie-crond/cronie, last push 2026-10-14), systemd.timer(5) (systemd repository), and flock(1) (util-linux).
Confirmed: day-of-month and day-of-week OR rule, `/etc/cron.d` and `/etc/crontab` user field, default environment (SHELL, LOGNAME, HOME), `MAILTO` rules, `CRON_TZ`, `%` handling, `*/N` step caveat, `crontab -T`, anacron period and delay behaviour, `Persistent=`, `flock -n`.
Removed as unconfirmed: the `/etc/cron.hourly` run-parts claim, claims about local mail delivery, the `env -i` test, `date +%u` wrapper advice, and statements about non-cronie crons.

Method: documentation, plus commands run 2026-11-01 in a Fedora 44 rootless Podman container (cronie 1.7.2, crond run in the foreground for a minute): crontab -T accepting a valid file and rejecting a bad minute, a missing field and a missing final newline; day-of-month OR day-of-week firing when only the weekday matched; SHELL, LOGNAME, HOME and own variables in the job environment; an unescaped % ending the command (no output file) versus \% and data after % reaching standard input; flock -n keeping a second instance from running, exit 1, and -E changing it. Corrected: /etc/crontab in cronie holds only variables and comments, not nothing. Observed: crontab -T accepts a comment after a variable setting, so it does not catch that mistake. Not run: anacron catch-up (anacron -T needs /var/spool/anacron), CRON_TZ, MAILTO delivery, systemd timers.
