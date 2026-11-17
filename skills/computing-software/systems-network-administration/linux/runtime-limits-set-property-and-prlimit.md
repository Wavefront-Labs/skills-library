---
id: computing-software.systems-network-administration.linux.runtime-limits-set-property-and-prlimit
name: runtime-limits-set-property-and-prlimit
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, set-property, prlimit, systemctl-set-property, ulimit, rlimit, runtime-limits, nofile]
level: practitioner
status: docs-checked
description: "Change resource limits on running services and processes without restarts: systemctl set-property (runtime vs persistent) for cgroup limits and prlimit for rlimits like nofile."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/prlimit.1.adoc
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemctl set-property and prlimit

## cgroup limits on a running unit
```bash
systemctl set-property --runtime app.service CPUQuota=150% MemoryMax=4G TasksMax=2000   # until reboot
systemctl set-property app.service CPUWeight=50 IOWeight=50                              # persistent
systemctl show app.service -p CPUQuotaPerSecUSec -p MemoryMax -p TasksMax
```
Changes are stored under `/etc/systemd/system.control/` (with `--runtime`, `/run/systemd/system.control/`).
`systemctl revert app.service` removes them; the man page says it also drops other drop-ins and masks, so check first.
Works on slices and scopes too (`user-1000.slice`, `session-3.scope`).
The man page says not all properties can change at runtime; many resource-control settings (systemd.resource-control) can.

## rlimits on a running process (prlimit)
```bash
prlimit --pid 4211                            # show all
prlimit --pid 4211 --nofile=65536:65536       # soft:hard
prlimit --pid 4211 --core=unlimited
cat /proc/4211/limits
```
Raising a hard limit needs privilege. An application may have read its limit at startup, so some only benefit after a restart.

## Make rlimits permanent
systemd service: `LimitNOFILE=65536` in a drop-in, then restart. Interactive users: `/etc/security/limits.conf` and the
`/etc/security/limits.d` directory, applied by pam_limits to login sessions.

## Gotchas
- `ulimit -n` in your shell changes nothing for an already-running daemon.
- `set-property` CPUQuota above 100% = more than one CPU.

## Verify
- [ ] `cat /proc/<pid>/limits` and the cgroup files (`memory.max`, `cpu.max`) show the new values.

## Checked

Checked 2026-10-27 against systemd man pages (systemd-oomd.service, oomd.conf, systemd.resource-control, systemctl, systemd.exec, systemd.unit, sysctl.d, tmpfiles.d, udev, systemd-delta, systemd-analyze), current main, 2026-10-27; util-linux prlimit(1) source; linux-pam limits.conf(5). Confirmed: set-property runtime/persistent behaviour and --runtime, system.control directories, revert, resource-control property names, LimitNOFILE in systemd.exec, prlimit --pid/--nofile/--core syntax with soft:hard and unlimited, limits.conf and limits.d. Removed or softened: claim that only resource-control properties can be set, capability name, container-runtime remark, exact drop-in file name.

Method: documentation only; no commands were run.
