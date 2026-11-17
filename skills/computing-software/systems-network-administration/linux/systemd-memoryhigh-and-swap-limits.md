---
id: computing-software.systems-network-administration.linux.systemd-memoryhigh-and-swap-limits
name: systemd-memoryhigh-and-swap-limits
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, memoryhigh, memoryswapmax, memorymax, memorylow, cgroup-v2, memory-throttling, systemd-resource-control]
level: advanced
status: docs-checked
description: "Throttle instead of OOM-kill with cgroup v2 memory controls: MemoryHigh vs MemoryMax, MemoryLow/Min protection, MemorySwapMax, memory.events and pressure readings."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files
  - https://facebookmicrosites.github.io/cgroup2/docs/memory-controller.html
  - https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MemoryHigh, MemoryMax and swap limits

## The knobs (cgroup v2, via systemd)
| Setting | File | Behaviour at the limit |
|---|---|---|
| `MemoryMax=` | memory.max | hard cap → if usage cannot be contained, the OOM killer is invoked inside the unit |
| `MemoryHigh=` | memory.high | throttling limit → processes are heavily slowed and memory is reclaimed aggressively (the main control mechanism) |
| `MemoryLow=` | memory.low | best-effort protection from reclaim |
| `MemoryMin=` | memory.min | protection from reclaim |
| `MemorySwapMax=` | memory.swap.max | absolute limit on swap usage (a percentage is relative to the system's swap size) |
| `MemoryZSwapMax=` | memory.zswap.max | zswap limit |

Pattern: set `MemoryHigh` below `MemoryMax` — systemd documents `MemoryHigh=` as the main control and `MemoryMax=` as the last line of defence.
```bash
systemctl set-property batch.service MemoryHigh=6G MemoryMax=7G MemorySwapMax=1G
systemctl set-property postgresql.service MemoryLow=8G     # protect DB cache from batch jobs
```
`MemoryMax=` also accepts a percentage of installed physical memory (e.g. `50%`).

## Watch it
```bash
CG=/sys/fs/cgroup/system.slice/batch.service
cat $CG/memory.current $CG/memory.swap.current
cat $CG/memory.events        # high = times processes were throttled and sent to direct reclaim, max, oom, oom_kill counters
cat $CG/memory.pressure      # pressure stall information for memory
systemd-cgtop -m
```

## Gotchas
- `MemoryHigh` too low makes the process crawl indefinitely (looks hung) — alert on `memory.pressure`.
- A cgroup's memory usage includes page cache, so file-heavy services can reach the limits through cache.
- `MemoryLimit=` is the deprecated v1-era setting; use `MemoryMax=` on cgroup v2.

## Verify
- [ ] Under a load test, `memory.events high` increases while `oom_kill` stays 0 and latency stays acceptable.

## Checked

Checked against the systemd `systemd.resource-control` and `systemd-cgtop` man sources and the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (cgroup-v2) on 2026-10-26. Confirmed: `MemoryMax=`, `MemoryHigh=` (main mechanism), `MemoryLow=`, `MemoryMin=`, `MemorySwapMax=` (percentage relative to swap size), `MemoryZSwapMax=`, percentage values for `MemoryMax=` relative to physical memory, `MemoryLimit=` listed as deprecated, `memory.events` `high`/`max`/`oom`/`oom_kill`, `memory.pressure`, `systemd-cgtop -m`. Removed: the 90% ratio, the stat-based cgroup v2 test and runtime flag examples.

Method: documentation only; no commands were run.
