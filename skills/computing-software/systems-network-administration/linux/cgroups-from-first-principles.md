---
id: computing-software.systems-network-administration.linux.cgroups-from-first-principles
name: cgroups-from-first-principles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cgroups, cgroup-v2, cpu-limit, memory-limit, oom, cpuset, io-weight, systemd-cgtop, systemd-run, docker, kubernetes, resource-control, sysadmin, containers]
level: advanced
status: docs-checked
description: "Limit CPU, memory, and IO by hand with cgroup v2 controllers in sysfs — the resource-control half of what container runtimes configure for you."
sources:
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
  - https://github.com/systemd/systemd/blob/main/man/kernel-command-line.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cgroups from first principles — resource limits, no runtime required

**Goal:** cap a process group's CPU, memory, and IO using cgroup v2's sysfs
interface directly, understand what each knob actually controls, and read
`systemd-cgtop`/OOM kill logs back to the cgroup responsible — the resource
side that pairs with namespaces (isolation) to make a "container."

## 1. Confirm v2 and find the hierarchy
```bash
mount | grep cgroup2                       # unified hierarchy, typically /sys/fs/cgroup
cat /sys/fs/cgroup/cgroup.controllers       # controllers available: cpu memory io pids ...
```
cgroup v2 uses a single unified hierarchy; v1's per-controller hierarchies are legacy and systemd has deprecated its v1 mode. If `cgroup.controllers`
doesn't exist, the box is still on v1 (`cat /proc/cgroups` instead) and the
file names below differ (`cpu.cfs_quota_us` etc.) — check which is in play
before copying commands.

## 2. Create a cgroup and move a process into it by hand
```bash
echo "+cpu +memory +io" > /sys/fs/cgroup/cgroup.subtree_control   # enable controllers for children of the root
mkdir /sys/fs/cgroup/myapp
echo $$ > /sys/fs/cgroup/myapp/cgroup.procs    # moves the current shell (and children) into it
cat /sys/fs/cgroup/myapp/cgroup.procs           # confirm membership
```
Every process belongs to exactly one cgroup at a time in v2 — moving a PID into
another cgroup removes it from the previous one. Controller files such as `cpu.max` and
`memory.max` only exist in a child cgroup after the controller is enabled in the parent's
`cgroup.subtree_control`, and they do not exist on the root cgroup. On systemd hosts prefer
`systemd-run` or unit properties (section 6) over creating cgroups by hand.

## 3. CPU limits
```bash
echo "200000 100000" > /sys/fs/cgroup/myapp/cpu.max   # 200ms CPU per 100ms period = 2 full cores
echo "max 100000" > /sys/fs/cgroup/myapp/cpu.max       # unlimited (default is "max 100000")
echo 512 > /sys/fs/cgroup/myapp/cpu.weight             # relative share vs siblings when CPU is contended (1-10000, default 100)
```
`cpu.max` is a **hard ceiling** (the process group literally cannot exceed
it, throttled even if the rest of the box is idle) — this is the well-known
"container has a 2-core limit, box has 32 idle cores, but the app still gets
throttled" complaint (`cpu.stat`'s `nr_throttled`/`throttled_usec` confirm
it). `cpu.weight` is **relative**, only matters under contention, and does
nothing when the box has spare capacity.

## 4. Memory limits and the OOM boundary
```bash
echo "512M" > /sys/fs/cgroup/myapp/memory.max     # hard limit — the OOM killer is invoked inside the cgroup when usage cannot be reduced
echo "400M" > /sys/fs/cgroup/myapp/memory.high    # throttle limit — processes are throttled and put under reclaim pressure, no OOM kill
cat /sys/fs/cgroup/myapp/memory.current
cat /sys/fs/cgroup/myapp/memory.events             # high, max, oom, oom_kill counters — the forensic trail
```
`memory.max` exceeded → the kernel's cgroup-aware OOM killer kills a process
*inside that cgroup*, confined to it — this is why one noisy container on a
shared host doesn't necessarily take down everything else, and why
`dmesg`/`journalctl -k | grep -i oom` after an incident should be checked for
which cgroup's `memory.max` the kill happened under, not just "the system ran
out of memory." `memory.high` is the gentler lever: set it below `memory.max`
to get back-pressure (reclaim, slower allocations) as an early warning before
a hard kill.

## 5. IO weight
```bash
echo "253:0 100" > /sys/fs/cgroup/myapp/io.weight   # major:minor device, weight 1-10000 (default 100)
cat /sys/fs/cgroup/myapp/io.stat                     # per-device rbytes/wbytes, rios/wios
```
Needs the `io` controller enabled and only has effect on contended devices —
like CPU weight, does nothing when the disk isn't busy. Find `major:minor`
with `lsblk -o NAME,MAJ:MIN`.

## 6. What systemd and Docker are actually doing for you
```bash
systemd-run --scope -p CPUQuota=50% -p MemoryMax=256M /usr/bin/stress --cpu 2
systemd-cgtop                                   # live view, grouped by cgroup, across the whole tree
systemctl show myapp.service -p MemoryMax -p CPUQuota
```
`systemd-run`'s `-p` properties and a systemd unit's `[Service]` resource
directives (`CPUQuota=`, `MemoryMax=`, `IOWeight=`) are a friendlier front
end that writes exactly the sysfs files shown above. Docker's `--cpus`,
`--memory`, `--memory-swap` flags do the same translation one layer further
out. Reading a `docker inspect`'s `HostConfig` resource fields next to
`/sys/fs/cgroup/.../docker-<id>.scope/` on the host makes the mapping
concrete.

## Gotchas
- `cgroup.procs` moves live processes; a **new** process forked after the
  move inherits the cgroup automatically (children stay with parent) unless
  something explicitly moves it elsewhere.
- Deleting a cgroup directory (`rmdir`) fails with `EBUSY` while any process
  is still in it — empty it (move members out, or let them exit) first.
- A cgroup's memory usage includes page cache, so `ps`/`top` RSS does not explain
  it; `memory.stat`'s `file`/`anon` breakdown does.
- Do not assume v1 is available: systemd deprecated the `systemd.unified_cgroup_hierarchy` kernel
  command-line argument in version 252, so tooling should target the v2 files shown here.

## Verify
- [ ] `cat cpu.stat` shows `nr_throttled` rising only when the app is genuinely CPU-bound above its quota, not during idle periods — confirms the limit is sized correctly.
- [ ] `memory.events`' `oom_kill` count correlates with actual incident timestamps, not silent background kills nobody investigated.
- [ ] `systemd-cgtop` / `docker stats` numbers match what the sysfs files for that cgroup report directly — no mystery gap.
- [ ] A deliberately undersized `memory.max` test gets killed inside its own cgroup (`memory.events` `oom_kill` rises), without affecting sibling cgroups.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (cgroup-v2) and the systemd `systemd.resource-control` and `kernel-command-line` man sources on 2026-10-26. Confirmed: `cpu.max` default and format, `cpu.weight` range 1-10000 default 100, `io.weight` range and default, `memory.max`/`memory.high` semantics, `memory.events` counters including `oom_kill`, `nr_throttled` in `cpu.stat`, one cgroup per process, `CPUQuota=`/`MemoryMax=`/`CPUQuota` mapping, `systemd.unified_cgroup_hierarchy` deprecated in systemd 252. Bug fixed: the hand-built example now enables controllers in `cgroup.subtree_control` first; without it the control files do not exist. Removed: systemd version-for-v2 claim and Docker/Kubernetes version claims.

Method: documentation only; no commands were run.
