---
id: computing-software.systems-network-administration.linux.pid-max-and-threads-max-limits
name: pid-max-and-threads-max-limits
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysctl, pid-max, threads-max, fork-resource-temporarily-unavailable, tasksmax, max-map-count, process-limits]
level: practitioner
status: docs-checked
description: "Diagnose 'fork: Resource temporarily unavailable': kernel.pid_max, kernel.threads-max, vm.max_map_count, systemd TasksMax and RLIMIT_NPROC, which one is hit, and safe values."
sources:
  - https://docs.kernel.org/admin-guide/sysctl/kernel.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
  - https://github.com/systemd/systemd/blob/main/man/systemd-system.conf.xml
  - https://github.com/systemd/systemd/blob/main/man/logind.conf.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pid_max, threads-max and friends

**Symptom:** `fork: retry: Resource temporarily unavailable`, `pthread_create failed (EAGAIN)`,
Java `unable to create native thread`. Several limits produce the same EAGAIN — find which.

## Limits, cheapest check first
```bash
ps -eLf | wc -l                           # threads system-wide
cat /proc/sys/kernel/pid_max              # PIDs at or above this value are not allocated
cat /proc/sys/kernel/threads-max          # set at boot so thread structures use at most 1/8 of RAM
systemctl show -p TasksMax -p TasksCurrent <unit>    # cgroup pids limit; DefaultTasksMax is 15% of the minimum of pid_max, threads-max and root pids.max
cat /sys/fs/cgroup/<path>/pids.max /sys/fs/cgroup/<path>/pids.events   # 'max' counter increments on hits
ulimit -u ; grep -i 'max processes' /proc/<pid>/limits                  # RLIMIT_NPROC per UID
cat /proc/sys/vm/max_map_count            # maximum memory map areas per process; default 65530
```

## Fix the right one
```ini
# /etc/sysctl.d/80-pids.conf
kernel.pid_max = 4194304
kernel.threads-max = 4194304
vm.max_map_count = 262144        # only if the application documents it
```
- Service: `systemctl edit app` → `[Service] TasksMax=infinity` (or a number).
- Users: a drop-in on `user-.slice` setting `TasksMax=`; `nproc` in `/etc/security/limits.d/` for RLIMIT_NPROC.

## Gotchas
- Raising limits can hide a thread leak; count threads per process first (`ps -eLf`).
- Container runtimes set their own pids limit per container, separate from the host sysctl.

## Verify
- [ ] The counter that was hitting (`pids.events max`, threads vs pid_max) no longer increases under load.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) and the systemd man sources (`systemd-system.conf`, `systemd.resource-control`, `logind.conf`) on 2026-10-26. Confirmed: `pid_max` semantics, `threads-max` 1/8-of-RAM rule and maximum, `max_map_count` default 65530, `DefaultTasksMax` = 15% of min(pid_max, threads-max, root pids.max), `TasksMax=` enables the pids controller. Found stale: `UserTasksMax=` is not documented in the current logind.conf page. Removed: distro pid_max defaults, the user-UID.slice 33% figure, the kernel log line, the container flag name.

Method: documentation only; no commands were run.
