---
id: computing-software.systems-network-administration.linux.userspace-oom-earlyoom-and-systemd-oomd
name: userspace-oom-earlyoom-and-systemd-oomd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, oom, oom-killer, earlyoom, systemd-oomd, psi, memory-pressure, managedoomswap, managedoompressure, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Kill runaway memory users before the box thrashes: systemd-oomd with PSI thresholds per slice, earlyoom on non-systemd-oomd hosts, exclusions, and reading their kill logs."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html
  - https://www.freedesktop.org/software/systemd/man/latest/oomd.conf.html
  - https://github.com/rfjakob/earlyoom/blob/master/README.md
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
  - https://github.com/rfjakob/earlyoom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Userspace OOM: systemd-oomd and earlyoom

**Goal:** the kernel OOM killer acts only when memory is fully exhausted — often after
minutes of thrashing with an unresponsive box. A userspace killer acts earlier, on pressure.

## 1. systemd-oomd
Needs a unified cgroup v2 hierarchy and a kernel with PSI (Linux 4.20+); swap is highly recommended so the system has time to react. It acts on cgroups that opt in:
```ini
# drop-in for the slice whose children may be killed, e.g. user.slice or a service
# systemctl edit user@.service   (or app.slice)
[Service]
ManagedOOMMemoryPressure=kill
ManagedOOMMemoryPressureLimit=50%       # fraction of a 10 s window in which all tasks in the cgroup were delayed
```
```ini
# /etc/systemd/oomd.conf.d/override.conf
[OOM]
SwapUsedLimit=90%                       # default; acts when both memory and swap use exceed it, on ManagedOOMSwap=kill cgroups
DefaultMemoryPressureLimit=60%            # default
DefaultMemoryPressureDurationSec=30s     # default
```
```bash
systemctl enable --now systemd-oomd
oomctl                                   # monitored cgroups, current pressure, thresholds
journalctl -u systemd-oomd               # kill decisions are logged here
```
Protect critical units: `ManagedOOMPreference=avoid` (or `omit`) on the unit;
`MemoryLow=`/`MemoryMin=` (systemd.resource-control) protect their memory from reclaim.

## 2. earlyoom (simple, any distro)
```bash
# /etc/default/earlyoom
EARLYOOM_ARGS="-m 5 -s 10 -r 60 --avoid '(^|/)(init|Xorg|ssh)$' --prefer '(^|/)(java|chromium)$' -n"
systemctl enable --now earlyoom
journalctl -u earlyoom
```
`-m 5 -s 10`: send SIGTERM when available RAM and free swap are both at or below those percentages; SIGKILL at the
second value of each option, which defaults to half. `-r` is the report interval in seconds, `-n` enables D-Bus
notifications. The victim is the process with the highest `oom_score` unless `--sort-by-rss` is used.

## 3. Choosing
| | systemd-oomd | earlyoom | kernel OOM |
|---|---|---|---|
| Trigger | PSI pressure / swap | free RAM+swap % | allocation failure |
| Kills | whole cgroup | one process | one process (by oom_score) |
| Best for | desktops, systemd-managed services | simple servers, older distros | always present as backstop |
Running both is redundant; pick one.

## Gotchas
- oomd kills **whole cgroups** — a user session or entire service, not one browser tab.
- The systemd documentation highly recommends swap for oomd; without it the system can livelock before oomd reacts.
- Too aggressive thresholds kill builds/compiles that are merely using memory productively.

## Verify
- [ ] `oomctl` lists the cgroups you expect, or `systemctl status earlyoom` shows thresholds.
- [ ] A deliberate memory hog inside a test unit is killed and logged while ssh stays responsive.

## Checked

Checked 2026-10-27 against systemd man pages (systemd-oomd.service, oomd.conf, systemd.resource-control, systemctl, systemd.exec, systemd.unit, sysctl.d, tmpfiles.d, udev, systemd-delta, systemd-analyze), current main, 2026-10-27; earlyoom README (rfjakob/earlyoom master). Confirmed: cgroup v2 and PSI (4.20) requirements, ManagedOOMMemoryPressure/Limit/Swap/Preference properties, oomd.conf defaults (SwapUsedLimit 90%, pressure 60%, duration 30 s), oomctl, earlyoom -m/-s/-r/-n/--avoid/--prefer flags, KILL_PERCENT default of half, /etc/default/earlyoom, oom_score victim selection. Removed or softened: distribution default claims, package install line, example log line, container OOM remark, stress-ng test details.

Method: documentation only; no commands were run.
