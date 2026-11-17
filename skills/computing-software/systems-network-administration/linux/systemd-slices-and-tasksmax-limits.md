---
id: computing-software.systems-network-administration.linux.systemd-slices-and-tasksmax-limits
name: systemd-slices-and-tasksmax-limits
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cgroups, systemd-slice, slice-units, tasksmax, pids-limit, resource-control, fork-bomb, systemd-cgls, systemd-cgtop, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Group services into custom systemd slices with shared CPU/memory/IO budgets, and cap process and thread counts with TasksMax, including the can't-fork failure it causes."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html#pid
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slices and TasksMax

**Goal:** put a group of services under one resource budget, and stop a runaway service
(or user) from exhausting PIDs for the whole machine.

## 1. The hierarchy
`-.slice` → `system.slice` (services), `user.slice` (`user-UID.slice` per login user),
`machine.slice` (VMs/containers). Slice names encode the path: `app-batch.slice` is a child
of `app.slice`.
```bash
systemd-cgls                             # tree
systemd-cgtop -m                         # live usage per cgroup, by memory
systemctl status app.slice
```

## 2. A custom slice
```ini
# /etc/systemd/system/batch.slice
[Unit]
Description=Batch jobs budget
[Slice]
CPUWeight=20          # relative CPU weight among siblings
MemoryHigh=6G         # throttle/reclaim above this
MemoryMax=8G          # hard limit for the whole group
IOWeight=20
TasksMax=2000
```
Put units in it: `Slice=batch.slice` in each `[Service]`, or ad hoc
`systemd-run --slice=batch.slice --unit=reindex /usr/local/bin/reindex`. Change live:
`systemctl set-property batch.slice MemoryMax=10G` (applied immediately and stored on disk; `--runtime` for temporary).

## 3. TasksMax (pids controller)
Limits the number of tasks (the pids controller). `DefaultTasksMax=` in `system.conf` defaults to 15% of the minimum of `kernel.pid_max`, `kernel.threads-max` and the root cgroup `pids.max`; `user-UID.slice` is capped at `TasksMax=33%` by systemd's default `user-.slice.d` drop-in.
```bash
systemctl show app -p TasksMax -p TasksCurrent
cat /sys/fs/cgroup/system.slice/app.service/pids.max /sys/fs/cgroup/system.slice/app.service/pids.current
systemctl set-property app.service TasksMax=8192
```
`LimitNPROC=` (RLIMIT_NPROC), `kernel.pid_max` and `kernel.threads-max` are separate limits that can give a similar symptom.

## Gotchas
- Limits on a slice are shared by everything inside; one hog still hurts its siblings in the slice.
- `TasksMax=infinity` removes protection against fork bombs; set a large finite number instead.


## Verify
- [ ] `systemd-cgls` shows your units under the new slice.
- [ ] `systemctl show <slice> -p MemoryMax -p TasksMax` reports the set values.
- [ ] A test fork loop inside a capped unit fails at TasksMax while the host stays responsive.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: slice naming (`foo-bar.slice` sits inside `foo.slice`) and default slices system/machine/user (`systemd.slice`); `systemd-run --slice=`; `systemd-cgtop -m` orders by memory; `CPUWeight=`, `MemoryHigh=`, `IOWeight=`, `TasksMax=` and the pids controller (`systemd.resource-control`, cgroup v2 `pids.max`/`pids.current`); `set-property` applies immediately, stores on disk and has `--runtime`; `DefaultTasksMax=` default; `TasksMax=infinity` means no limit; the 33% user-slice default. Removed the kernel log message, Java error strings, the cgroup v1 remark, the system.control path and the default CPU weight value.

Method: documentation only; no commands were run.
