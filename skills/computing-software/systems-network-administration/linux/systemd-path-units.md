---
id: computing-software.systems-network-administration.linux.systemd-path-units
name: systemd-path-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, path-unit, pathchanged, pathmodified, directorynotempty, file-watch-trigger, inotify]
level: practitioner
status: docs-checked
description: "Trigger a service when files change using systemd .path units: PathChanged vs PathModified vs DirectoryNotEmpty, unit pairing, rate limits and inotify caveats."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd .path units

**Goal:** run a job when a file appears or changes (drop-folder processing, reload on config change)
without a polling cron loop.

## Pair of units
`/etc/systemd/system/incoming.path`
```ini
[Unit]
Description=Watch the upload drop folder
[Path]
DirectoryNotEmpty=/srv/incoming
# PathChanged=/etc/myapp/config.yml     # fires when a file opened for writing is closed
# PathModified=/etc/myapp/config.yml    # also fires on simple writes
# PathExists=/run/myapp/trigger         # fires while the path exists
# PathExistsGlob=/srv/incoming/*.csv
Unit=incoming.service                    # default: same name with .service
MakeDirectory=yes
DirectoryMode=0750
TriggerLimitIntervalSec=10s
TriggerLimitBurst=20
[Install]
WantedBy=multi-user.target
```
`/etc/systemd/system/incoming.service`
```ini
[Service]
Type=oneshot
ExecStart=/usr/local/bin/process-incoming
```
```bash
systemctl daemon-reload && systemctl enable --now incoming.path
systemctl list-units --type=path
```

## Semantics that bite
- **DirectoryNotEmpty / PathExists / PathExistsGlob** are checked again right after the triggered service ends, so the service must empty the directory (or remove the path) or it restarts in a loop until the start rate limit (`StartLimitIntervalSec=`/`StartLimitBurst=` on the service) is hit; that failure is propagated to the path unit.
- Path units use inotify, so they cannot see changes made by other machines on remote NFS file systems.
- Process everything present in the directory on each run rather than assuming one new file per trigger.

## Verify
- [ ] `touch /srv/incoming/test` → `journalctl -u incoming.service` shows a run and the folder ends empty.
- [ ] `systemctl status incoming.path` stays `active (waiting)` after the burst.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `PathExists=`, `PathExistsGlob=`, `PathChanged=` (activated when a file opened for writing is closed), `PathModified=` (also on simple writes), `DirectoryNotEmpty=`, `MakeDirectory=`, `DirectoryMode=`, `TriggerLimitIntervalSec=`/`TriggerLimitBurst=` (default interval 2s), `Unit=`; the re-check after the service ends and the start rate limit propagating to the path unit; the inotify/NFS limitation. Removed claims about parent-directory watching, bind mounts and rename handling.

Method: documentation only; no commands were run.
