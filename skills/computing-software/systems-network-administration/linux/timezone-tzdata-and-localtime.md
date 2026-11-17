---
id: computing-software.systems-network-administration.linux.timezone-tzdata-and-localtime
name: timezone-tzdata-and-localtime
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, timezone, tzdata, etc-localtime, zoneinfo, timedatectl, tz-variable, dst, zdump, containers-timezone, sysadmin]
level: practitioner
status: docs-checked
description: "Set and verify time zones on Linux: /etc/localtime and zoneinfo, timedatectl set-timezone, per-process TZ, keeping tzdata current for DST changes, and containers."
sources:
  - https://github.com/eggert/tz/blob/main/zdump.8
  - https://github.com/eggert/tz/blob/main/tzfile.5
  - https://github.com/systemd/systemd/blob/main/man/timedatectl.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd.time.xml
  - https://github.com/cronie-crond/cronie/blob/master/man/crontab.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones: tzdata and /etc/localtime

**Goal:** hosts show the intended local time, DST changes happen correctly, and you know
which layer (system, process, container) decides.

## 1. How Linux decides local time
- The system clock counts UTC; local time is derived from the time zone data.
- System default: `/etc/localtime` — a **symlink** to `/usr/share/zoneinfo/<Area>/<City>` (compiled tzdata rules).
- Per process: the `TZ` environment variable overrides it (`TZ=America/New_York date`).

## 2. Set and check
```bash
timedatectl                                   # Local time, Universal time, Time zone, NTP sync
timedatectl list-timezones | grep -i london
timedatectl set-timezone Europe/London
ls -l /etc/localtime                          # -> ../usr/share/zoneinfo/Europe/London
# without systemd:
ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime
```
Servers: many teams standardise on `Etc/UTC` — logs across regions line up and DST never shifts
cron jobs. Present local time in applications instead.

## 3. Keep tzdata current
Governments change DST rules at short notice; the `tzdata` package carries IANA's rules.
```bash
rpm -q tzdata / dpkg -l tzdata
zdump -v /usr/share/zoneinfo/Europe/London | grep 2026       # transitions this year
```
- Update the package (normal security/updates stream) before a rule change takes effect.
- Already-running processes may have loaded the rules earlier; restart long-lived services after a tzdata update, and check runtimes that ship their own time zone data.

## 4. Cron, systemd timers and DST
- cron runs in the system time zone; during a DST change, jobs scheduled in the skipped hour never match and jobs in a repeated hour can run twice (crontab(5)).
  Use `CRON_TZ=UTC` (cronie) per crontab, or schedule outside the transition hour.
- systemd timers: `OnCalendar=*-*-* 02:30 Europe/London` accepts an explicit zone.

## 5. Containers
A container does not inherit your zone setting automatically: check whether the image contains tzdata and whether `TZ` is set there.

## Gotchas
- Changing the zone doesn't change the clock; it only changes display. Never "fix" a wrong time by changing the zone.
- Databases and application runtimes may have their own time zone settings.

## Verify
- [ ] `timedatectl` shows the intended zone with correct UTC offset; `date` and `date -u` differ by that offset.
- [ ] `zdump -v` shows the expected DST transitions for the current year (tzdata is current).

## Checked

2026-10-26. tz repository (eggert/tz) zdump(8) and tzfile(5) pages (zdump -v verbose mode, TZ strings); timedatectl(1): set-timezone changes the /etc/localtime symlink and list-timezones; systemd.time(7): OnCalendar accepts an IANA time zone and defaults to the current one; cronie crontab(5): CRON_TZ and the DST conversion warnings (skipped hours never match, repeated hours run twice). Removed Debian /etc/timezone, Java tzupdater, container bind-mount advice and other statements that no fetched source covers. tz theory.html: the TZ environment variable selects the zone for a process; zoneinfo directory layout. The link path shown for /etc/localtime is an example.

Method: documentation only; no commands were run.
