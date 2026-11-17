---
id: computing-software.systems-network-administration.linux.systemd-template-instantiated-units
name: systemd-template-instantiated-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, template-unit, instantiated-units, unit-specifiers, systemd-instance, at-sign-units]
level: practitioner
status: docs-checked
description: "Write and run systemd template units (name@.service): %i/%I specifiers, per-instance drop-ins, enabling instances, escaping with systemd-escape and DefaultInstance."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-escape.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template and instantiated units

**Goal:** one unit file, many instances — `openvpn-server@site1`, `worker@1..8`, `getty@tty2`.

## Template
`/etc/systemd/system/worker@.service`
```ini
[Unit]
Description=Queue worker %i
After=network-online.target
Wants=network-online.target
[Service]
User=worker
EnvironmentFile=-/etc/worker/%i.env
ExecStart=/usr/local/bin/worker --queue=%i
Restart=on-failure
[Install]
WantedBy=multi-user.target
DefaultInstance=default
```
```bash
systemctl daemon-reload
systemctl enable --now worker@emails.service worker@reports.service
systemctl start worker@{1..4}.service     # brace expansion is the shell's, not systemd's
systemctl list-units 'worker@*'
systemctl stop 'worker@*'                 # globs match loaded units
```

## Specifiers
| | |
|---|---|
| `%i` | instance name escaped as given |
| `%I` | unescaped instance (`-` → `/` etc.) |
| `%n` / `%N` | full unit name / without suffix |
| `%p` | prefix (`worker`) |
| `%H` / `%h` | host name / user home (user units) |

Paths as instances need escaping: `systemd-escape --path /srv/data/a` → `srv-data-a`; then
`backup@srv-data-a.service` with `ExecStart=/usr/bin/backup %I` gets `/srv/data/a` back.

## Per-instance overrides
`systemctl edit worker@reports.service` → drop-in in `worker@reports.service.d/` (only that instance);
`worker@.service.d/` applies to all.

## Gotchas
- Enabling the bare template without an instance fails unless `DefaultInstance=` is set.
- `WantedBy=` symlinks are created per instance in `multi-user.target.wants/worker@emails.service`.

## Verify
- [ ] `systemctl status worker@emails` shows `--queue=emails` in the command line; reboot brings the enabled instances back.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: template naming and `%i`/`%I`/`%n`/`%N`/`%p`/`%H`/`%h` specifiers, `DefaultInstance=` for enabling a bare template, instance symlinks created in the `.wants/` directory of the listed unit (`systemd.unit`); `systemd-escape --path` and `--suffix`; `systemctl` accepts glob patterns for units in memory. Removed one unverified escaping gotcha.

Method: documentation only; no commands were run.
