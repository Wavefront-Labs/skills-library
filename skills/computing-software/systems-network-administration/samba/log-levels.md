---
id: computing-software.systems-network-administration.samba.log-levels
name: log-levels
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, log-levels, log-level, debug-classes, logging, troubleshooting]
level: practitioner
status: docs-checked
description: "Control Samba logging: log level with debug classes, log file, max log size, logging backends, the -d override, and runtime changes via smbcontrol."
sources:
  - https://wiki.samba.org/index.php/Setting_the_Samba_Log_Level
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
  - https://www.samba.org/samba/docs/current/man-html/smbcontrol.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# log levels
smb.conf:
- `log level` default `0`. `log level = 3` sets all classes; per class: `log level = 3 passdb:5 auth:5` (general 3, passdb and auth at 5).
- `log file`: no default; takes the standard substitutions, so you can have a separate file per user or machine (for example `%m`).
- `max log size`: default `5000` KB; at the limit the file rotates to `.old`; `0` means no limit.
- `logging`: default empty; list of backends written backend[:option][@loglevel] (syslog, file, systemd, lttng, gpfs, ringbuf; some need extra libraries); example `logging = syslog@1 file`. When set it overrides the `syslog` and `syslog only` parameters.

Command-line override: `-d 0-10` beats smb.conf (`net ads join -U administrator -d 1`). Level 0 logs only critical errors; 1 suits day-to-day running; above 1 is for investigating problems; above 3 is for developers and produces huge logs. `-l/--log-basename` sets the log directory, with `.progname` appended (log.smbclient, log.smbd); `--debug-stdout` sends output to stdout instead of stderr (smbcontrol page).

Runtime changes without restart:
```
smbcontrol smbd debug 3
smbcontrol winbindd debug 3
smbcontrol smbd debuglevel
```
The parent relays the level to its children.

Run winbindd in the foreground for live output with `winbindd -i`.

Gotcha: restore the level afterwards; high levels generate huge amounts of log data.

## Checked

2026-11-04. Confirmed against the Samba wiki Setting the Samba Log Level page: log level = 3, the passdb and auth class example, the -d override with the net ads join example. Confirmed against smb.conf(5): log level default 0, log file (no default, substitutions), max log size (KB, .old rename, 0 no limit, default 5000), logging syntax, backends and the override of syslog; against smbcontrol(1): -d 0-10, level guidance, --debug-stdout, -l, debug and debuglevel messages and the parent rebroadcast to children; winbindd(8): -i. Removed samba -i and smbd -i (not fetched), the /var/log/samba path example and the claim that high levels slow smbd.
Method: documentation only; no commands were run.
