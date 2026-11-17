---
id: computing-software.systems-network-administration.linux.journalctl-filtering-and-boots
name: journalctl-filtering-and-boots
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, journald, journalctl, journalctl-filtering, since-until, journal-priority, list-boots, journal-boots, persistent-journal, journal-fields, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Find the log lines that matter with journalctl: filter by unit, time window, priority, PID, field and boot, list previous boots, and make the journal persistent so they exist."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html
  - https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# journalctl: filtering and per-boot logs

**Goal:** go from "something broke around 3am, maybe last boot" to the exact lines in one or
two commands.

## 1. By unit, time, priority
```bash
journalctl -u nginx -u php-fpm --since "2026-10-16 02:30" --until "2026-10-16 03:15"
journalctl -u sshd --since "1 hour ago"       # relative; also "yesterday", "today"
journalctl -p err -b                           # priority err and worse (0 emerg … 3 err), this boot
journalctl -p warning..err                     # a range
journalctl -k -b -1                            # kernel ring buffer of the previous boot
journalctl -f -u app                           # follow
journalctl -n 100 --no-pager -u app            # last 100, script-friendly
```
Priorities: 0 emerg, 1 alert, 2 crit, 3 err, 4 warning, 5 notice, 6 info, 7 debug.

## 2. By field (exact match, fast — uses indexes)
```bash
journalctl _PID=1234
journalctl _UID=1001 _COMM=python3            # fields ANDed
journalctl _SYSTEMD_UNIT=app.service + _COMM=cron   # + = OR between groups
journalctl SYSLOG_IDENTIFIER=sudo
journalctl /usr/sbin/sshd                     # by executable path
journalctl -F _SYSTEMD_UNIT                   # list values a field takes (discover units)
journalctl -g 'timeout|refused' -u app        # PCRE grep inside messages (case-insensitive if lowercase)
```
`journalctl -o verbose -n 1 -u app` shows every field of an entry; `-o json` / `-o cat` /
`-o short-iso-precise` for scripts and correlation with other hosts.

## 3. Boots
```bash
journalctl --list-boots                 # idx, boot ID, first/last entry time
journalctl -b                           # current boot
journalctl -b -1 -p err                 # previous boot's errors
journalctl -b 3f8a…                     # by boot ID
journalctl -b -1 -n 50                  # the last lines before the previous shutdown/crash
```

## 4. Make history exist (persistent journal)
Default `Storage=auto` behaves like `persistent` only if `/var/log/journal` exists; otherwise
the journal lives in `/run` and is lost on reboot.
```bash
mkdir -p /var/log/journal && systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald          # or set Storage=persistent in journald.conf
journalctl --disk-usage
```

## Gotchas
- Non-root users only see their own entries unless in `systemd-journal`, `adm` or `wheel`.
- `--since` uses local time; mixing hosts in different zones → use `-o short-iso` or `--utc`.
- Rate limiting (`RateLimitIntervalSec=`/`RateLimitBurst=` in `journald.conf`) drops further messages from a chatty service within the interval.

## Verify
- [ ] `journalctl --list-boots` shows more than one boot after a reboot (persistence works).
- [ ] Your filter returns the event you know happened and nothing outside the time window.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `-g`/`--grep=` uses PCRE2 and is case-insensitive when the pattern is all lowercase; `-p` accepts a level or `FROM..TO` range and a single level includes more important ones; `--list-boots`, `-b`, `-k`, `-F`, `--utc`, `-m`, `-D`, `--file`, `--vacuum-time`, `--disk-usage` exist; a file path argument matches `_EXE=` for executables; groups `systemd-journal`, `adm`, `wheel` can read all journals; `Storage=` values and the `auto` rule; `RateLimitBurst=` in `journald.conf`. Removed the RHEL claim, the crash-detection heuristic and the cgroup remark because no documentation states them.

Method: documentation only; no commands were run.
