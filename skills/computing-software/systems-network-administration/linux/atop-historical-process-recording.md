---
id: computing-software.systems-network-administration.linux.atop-historical-process-recording
name: atop-historical-process-recording
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, atop, performance, historical-metrics, atopsar, process-accounting, post-mortem]
level: practitioner
status: docs-checked
description: "Record and replay per-process resource history with atop: the atop service and logs, reading a past minute with atop -r, key views, atopsar reports and retention."
sources:
  - https://github.com/Atoptool/atop/blob/master/man/atop.1
  - https://github.com/Atoptool/atop/blob/master/man/atopsar.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# atop for historical per-process data

**Why:** sar tells you the box was at 100% CPU at 03:12; atop tells you **which process** — including
ones that started and exited between samples (via process accounting).

## Install and record
```bash
# install the atop package from your distribution
systemctl enable --now atop atopacct      # logs to /var/log/atop/atop_YYYYMMDD, 10-min samples by default
# interval/retention: LOGINTERVAL (default 600 s) and LOGGENERATIONS (default 28 days), overridden in /etc/default/atop
```

## Replay
```bash
atop -r /var/log/atop/atop_20261017 -b 03:05      # open at 03:05
#   t / T  next / previous sample     b  jump to time
```
Views (keys): `g` generic, `m` memory, `d` disk, `n` network (needs netatop), `c` command lines, `s` scheduling,
`v` various, `p` aggregate per program, `u` per user, `C/M/D` sort by CPU/memory/disk.

## Reports
```bash
atopsar -r /var/log/atop/atop_20261017 -c -b 02:00 -e 04:00   # CPU
atopsar -d ; atopsar -m ; atopsar -O (top processes per interval)
atop -r file -P CPU,PRG > parsable.txt                        # machine-readable for scripts
```

## Gotchas
- Raw logs are compressed binary files; `atopconvert` converts them between versions (see its man page).
- Without the accounting daemon (`atopacct` service, atopacctd(8)), short-lived processes can be missed.
- Disk-full incidents: `/var/log/atop` growth itself — set generations.

## Verify
- [ ] `ls /var/log/atop` grows daily; `atop -r` at an incident time shows the top consumer by name.

## Checked

Checked 2026-10-27 against atop and atopsar man pages and the packaged atop.daily script (Atoptool/atop master), 2026-10-27. Confirmed: default 600 s interval, 28-generation retention and /var/log/atop location, LOGINTERVAL/LOGGENERATIONS variables overridable in /etc/default/atop, atop -r with -b/-e and -P labels, branch/next/previous keys, view keys, netatop requirement for network view, atopsar -c/-d/-m/-O options, atopacctd purpose. Removed or softened: yesterday shortcut, 60 s recommendation and storage estimate, highlighting and exited-process remarks, version-specific log claim.

Method: documentation only; no commands were run.
