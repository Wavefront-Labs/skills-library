---
id: computing-software.systems-network-administration.linux.proc-sys-dev-run-pseudo-filesystems
name: proc-sys-dev-run-pseudo-filesystems
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pseudo-filesystems, run-directory, procfs, sysfs, devtmpfs, tmpfs, fhs, lpic-1]
level: practitioner
status: docs-checked
description: "Know the virtual filesystems on every Linux box: /proc process and kernel interfaces, /sys device model, /dev devtmpfs, /run runtime state, /dev/shm, and what is safe to write."
sources:
  - https://docs.kernel.org/filesystems/proc.html
  - https://docs.kernel.org/filesystems/sysfs.html
  - https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03s15.html
  - https://www.freedesktop.org/software/systemd/man/latest/file-hierarchy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# /proc, /sys, /dev and /run

```bash
findmnt -t proc,sysfs,devtmpfs,tmpfs,cgroup2,securityfs,debugfs
```
| Mount | Type | Contents | Persistent? |
|---|---|---|---|
| `/proc` | proc | per-PID dirs (`status`, `fd/`, `maps`, `environ`, `limits`), kernel info (`meminfo`, `cpuinfo`, `cmdline`, `mounts`, `interrupts`), tunables `/proc/sys` | no |
| `/sys` | sysfs | device model: `/sys/block`, `/sys/class/net`, `/sys/bus/pci`, module params `/sys/module/*/parameters` | no |
| `/dev` | devtmpfs | device nodes created by the kernel, permissions/symlinks by udev | no |
| `/run` | tmpfs | PID files, sockets, runtime state (`/run/systemd`, `/run/user/<uid>`) | cleared at boot |
| `/dev/shm` | tmpfs | POSIX shared memory | cleared at boot |
| `/tmp` | tmpfs or disk | depends on distro | maybe |

## Writing to them
- `/proc/sys/...` and `/sys/...` writes change the running kernel immediately and are lost at reboot:
  `echo 1 > /proc/sys/net/ipv4/ip_forward`, `echo mq-deadline > /sys/block/sda/queue/scheduler`.
  Persist via `sysctl.d`, udev rules or tmpfiles.d (`w` lines, for example `w- /proc/sys/vm/swappiness - - - - 10`).
- `/proc/<pid>/` is read-only mostly (except `oom_score_adj`, `comm`, ...).

## Practical uses
`cat /proc/cmdline`, `/proc/loadavg`, `/proc/pressure/*`, `ls -l /proc/<pid>/cwd`, `/proc/net/dev`, `/sys/block/<dev>/queue/scheduler`.

## Gotchas
- `/run` is a size-limited tmpfs; apps writing logs there can fill it.
- `hidepid=2` (invisible) mount option on /proc hides other users' `/proc/<pid>` directories; `gid=` names a group that is exempt.

## Verify
- [ ] You can name where to read or set a given runtime value and how to make it persistent.

## Checked

Checked 2026-10-27 against Linux kernel documentation (filesystems/proc, filesystems/sysfs, accounting/psi, block/switching-sched) and systemd tmpfiles.d(5), current master, 2026-10-27. Confirmed: hidepid modes and gid=, /proc/pressure files, sysfs layout (devices, block, bus, class), IO scheduler switching via /sys/block/DEV/queue/scheduler, tmpfiles.d w lines writing to /proc/sys, writable oom_score_adj. Removed or softened: /sys/fs/cgroup listing, /var/run symlink note, tmp.mount name, tuned, /run size percentage, container masking remark, zero-size file advice, example sysfs paths for speed and thermal, Ubuntu reboot-required file.

Method: documentation only; no commands were run.
