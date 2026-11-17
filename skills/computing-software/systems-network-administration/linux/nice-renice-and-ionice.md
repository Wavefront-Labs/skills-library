---
id: computing-software.systems-network-administration.linux.nice-renice-and-ionice
name: nice-renice-and-ionice
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nice, renice, nice-renice, ionice, cpu-priority, io-priority, io-scheduler, chrt, scheduling, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Keep batch jobs from starving interactive work: CPU niceness with nice/renice, I/O classes with ionice, which schedulers honour them, and the systemd equivalents."
sources:
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/renice.1.adoc
  - https://github.com/util-linux/util-linux/blob/master/schedutils/ionice.1.adoc
  - https://github.com/util-linux/util-linux/blob/master/schedutils/chrt.1.adoc
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml
  - https://www.kernel.org/doc/html/latest/scheduler/sched-rt-group.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nice, renice and ionice

**Goal:** run backups, compiles and reindexing at low priority so production latency doesn't
suffer — or raise priority of something critical.

## 1. CPU: nice / renice
Niceness −20 (highest priority) … 19 (lowest); 0 is the base priority. Unprivileged users can only raise the nice
value, irreversibly unless they have a suitable nice resource limit (renice(1)).
```bash
nice -n 19 tar czf /backup/home.tgz /home     # start low
renice -n 10 -p 1234                          # set absolute niceness 10 (util-linux; see note)
renice -n 5 -u builduser                      # all of a user's processes
renice -n -5 -g 4321                          # process group (root)
```
In util-linux `renice`, `-n` sets an absolute value unless `POSIXLY_CORRECT` is set; `--relative` always applies a delta.

## 2. I/O: ionice
Classes: `1` realtime (can starve others), `2` best-effort with level 0 (high)…7 (low; the default level is 4),
`3` idle (disk time only when nobody else asked for it for a grace period).
```bash
ionice -c3 -p 1234                    # idle class
ionice -c2 -n7 rsync -a /src /dst     # start best-effort lowest
nice -n19 ionice -c3 updatedb         # both
ionice -p 1234                        # show
```
If the active I/O scheduler does not implement I/O priorities they have no effect; cgroup I/O
controls (`IOWeight=` in systemd.resource-control) are the alternative.

## 3. In systemd units (persistent)
```ini
[Service]
Nice=10
IOSchedulingClass=idle          # or best-effort + IOSchedulingPriority=7
CPUSchedulingPolicy=batch       # other, batch, idle, fifo, rr or ext
CPUWeight=20                    # cgroup v2 CPU share (default 100)
IOWeight=10
```
For cron jobs: `nice -n19 ionice -c3 /usr/local/bin/job`.

## 4. Real-time (rarely)
`chrt -f -p 50 1234` (SCHED_FIFO; changing scheduling attributes needs `CAP_SYS_NICE`) — a runaway RT task can starve
other work; `/proc/sys/kernel/sched_rt_runtime_us` is the global limit on real-time time per period. Only for
audio/industrial control-type loads.

## Gotchas
- Lowering priority of a process holding a lock others need can make things slower (priority inversion).
- `nice` of a disk-bound job does nothing for disk contention — that's what ionice/IOWeight is for.

## Verify
- [ ] `ps -o ni,cmd` and `ionice -p` show the intended values.
- [ ] Under load, the batch job yields to the important workload (compare latency with and without).

## Checked

2026-10-26. util-linux master (last commit 2026-10-26): renice -n absolute-versus-relative behaviour and the unprivileged-user rule; ionice classes, levels 0-7, default level 4 and idle grace period; chrt CAP_SYS_NICE and -f. systemd man pages: Nice=, IOSchedulingClass=, IOSchedulingPriority=, CPUSchedulingPolicy= values, CPUWeight= default 100. Kernel sched-rt-group documentation: sched_rt_runtime_us. Removed unconfirmed statements about CFS/EEVDF, autogroup, which I/O schedulers honour priorities, the 5 percent figure, inheritance and pidstat.

Method: documentation only; no commands were run.
