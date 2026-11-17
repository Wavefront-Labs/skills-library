---
id: computing-software.systems-network-administration.linux.cron-timezone-and-dst
name: cron-timezone-and-dst
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cron, cron-tz, crontab, timezone, daylight-saving-time, cronie, utc]
level: practitioner
status: docs-checked
description: "Control which timezone cron jobs run in: system TZ, CRON_TZ and TZ in crontabs (cronie vs Debian cron), DST skipped and repeated hours, and running servers on UTC."
sources:
  - https://github.com/cronie-crond/cronie/blob/master/man/crontab.5
  - https://github.com/cronie-crond/cronie/blob/master/man/cron.8
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cron, timezones and DST

## Which timezone?
cron evaluates schedules in the daemon's local time zone unless a crontab sets `CRON_TZ`. cronie treats a clock or time zone change of more than 3 hours as a correction and uses the new time immediately (cron(8)).

## Per-crontab timezone
- **cronie**: `CRON_TZ` "specifies the time zone specific for the cron table"; enter the times in that zone. The cron log still
  uses the daemon's local time zone (crontab(5)).
- Other cron implementations: check `man 5 crontab` on your release. A systemd timer can name a zone in `OnCalendar=`
  (for example `... Europe/London`, systemd.time(7)).
```
CRON_TZ=America/New_York
0 9 * * 1-5  /usr/local/bin/market-open.sh
```

## DST behaviour (cronie)
- cron(8): when time moves one hour forward, jobs that would have run in the skipped interval run immediately; when it moves
  backward, running the same job twice is avoided. This applies to jobs at a specific time and jobs with a granularity of more than
  one hour; more frequent jobs are scheduled normally.
- crontab(5) still notes that times that do not exist never match and times that occur twice can match twice; treat the
  behaviour as implementation-specific and avoid critical jobs in the changeover hours.

## Recommendations
- Servers: a UTC system time zone avoids DST changes for cron schedules.
- Business-time jobs: express in the business TZ explicitly (CRON_TZ or systemd timer TZ suffix).
- Document the TZ in a comment above each job.

## Verify
- [ ] `timedatectl` confirms the system time zone; the job's log timestamps match the intended time after a DST change.

## Checked

Checked against cronie cron(8) and crontab(5) (cronie-crond/cronie, last push 2026-10-14) and systemd.time(5) (systemd repository).
Confirmed: `CRON_TZ` meaning, DST handling paragraph in cron(8) (forward jump runs skipped jobs immediately, backward jump avoids duplicates, more than 3 hours treated as a correction), the contrary note in crontab(5), systemd timezone suffix in calendar events.
Fixed: changing the system time zone does not require restarting cron (cron(8) says the new time is used immediately for changes over 3 hours). Removed as unconfirmed: the claim that `TZ=` affects only the job environment, Debian/Ubuntu vixie-cron statements, the 01:00-03:00 rule and the systemd unit name.

Method: documentation only; no commands were run.
