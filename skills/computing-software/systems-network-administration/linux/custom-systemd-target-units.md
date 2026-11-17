---
id: computing-software.systems-network-administration.linux.custom-systemd-target-units
name: custom-systemd-target-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, systemd-targets, custom-target, target-unit, allowisolate, partof, service-grouping, maintenance-mode, sysadmin]
level: practitioner
status: docs-checked
description: "Group services under your own .target: start/stop an application stack as one, build an isolatable maintenance mode, and wire it into boot with WantedBy and PartOf."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.special.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom target units

**Goal:** treat a set of services (app + workers + scheduler) as one thing you can start,
stop, enable and isolate.

## 1. A stack target
```ini
# /etc/systemd/system/myapp.target
[Unit]
Description=MyApp stack
Requires=network-online.target
After=network-online.target
[Install]
WantedBy=multi-user.target
```
Each member:
```ini
# /etc/systemd/system/myapp-web.service  (and myapp-worker.service, …)
[Unit]
PartOf=myapp.target          # stop/restart of the target propagates here
After=network-online.target
[Service]
ExecStart=/opt/myapp/bin/web
[Install]
WantedBy=myapp.target        # enable links it into myapp.target.wants/
```
```bash
systemctl daemon-reload
systemctl enable myapp-web myapp-worker myapp.target
systemctl start myapp.target         # starts members
systemctl restart myapp.target       # PartOf= makes members restart too
systemctl stop myapp.target          # PartOf= makes members stop
systemctl list-dependencies myapp.target
```
`Wants=` (from `WantedBy=`) only propagates *start*; `PartOf=` is what makes *stop/restart*
follow the target. `BindsTo=` would also stop members if the target vanishes unexpectedly.

## 2. An isolatable maintenance mode
```ini
# /etc/systemd/system/maintenance.target
[Unit]
Description=Maintenance (network + ssh only)
Requires=basic.target network-online.target sshd.service
After=basic.target network-online.target sshd.service
AllowIsolate=yes
```
`systemctl isolate maintenance.target` stops every unit not pulled in by it (your app,
cron, web server) while keeping SSH; `systemctl isolate multi-user.target` returns.
The unit name of the SSH daemon varies by distribution. Test from a console first: isolating stops everything the target does not pull in.

## 3. Boot into it
`systemctl set-default maintenance.target`, or one boot with kernel argument
`systemd.unit=maintenance.target`.

## Gotchas
- Targets run no processes; check the members, or use `Requires=` from the target to its members so failures show up.
- Dependencies (`Wants=`, `Requires=`) are separate from ordering: add `After=` on the members if something must wait for the whole stack.

## Verify
- [ ] `systemctl stop myapp.target` leaves no member active (`systemctl list-units 'myapp-*'`).
- [ ] After reboot all members are active and `systemctl is-active myapp.target` is active.
- [ ] `systemctl isolate maintenance.target` keeps your SSH session alive (test on console first).

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `PartOf=` propagates stop and restart only, `Wants=`/`WantedBy=` start only, `BindsTo=` semantics, `AllowIsolate=` and `systemctl isolate` stopping other units (`systemd.unit`, `systemctl`); `systemd.unit=` on the kernel command line; `systemctl set-default`. Removed unverified lock-out and status remarks.

Method: documentation only; no commands were run.
