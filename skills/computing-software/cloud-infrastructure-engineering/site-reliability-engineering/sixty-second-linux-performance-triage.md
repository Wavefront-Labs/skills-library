---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.sixty-second-linux-performance-triage
name: sixty-second-linux-performance-triage
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, troubleshooting, linux-performance-triage, sixty-second-analysis, use-method, performance]
level: practitioner
status: draft
description: "Triage a slow Linux host in 60 seconds with Brendan Gregg's ten commands (uptime, dmesg, vmstat, mpstat, pidstat, iostat, free, sar, top) and read each output."
sources: ["https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55", "https://www.brendangregg.com/usemethod.html", "https://www.brendangregg.com/linuxperf.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 60-second Linux performance triage

**Goal:** in the first minute on a misbehaving host, find which resource is saturated or erroring.

## The commands (Netflix, Brendan Gregg)
```bash
uptime                  # load averages 1/5/15 min: rising or falling?
dmesg -T | tail         # OOM kills, TCP drops, disk errors
vmstat 1                # r (run queue > CPUs = saturation), si/so (swapping), us/sy/wa/st
mpstat -P ALL 1         # one hot CPU = single-threaded bottleneck
pidstat 1               # which processes use CPU
iostat -xz 1            # await, %util (near 100% = saturated device), avgqu-sz
free -m                 # available memory, buffers/cache
sar -n DEV 1            # network throughput vs NIC limits
sar -n TCP,ETCP 1       # active/passive conns, retrans/s (network trouble)
top                     # overview sanity check
```

## Reading key fields
- `vmstat`: `r` larger than CPU count = CPU saturation; `wa` high = waiting on I/O; `st` (steal) high on VMs = noisy neighbour/oversubscribed host; nonzero `si/so` = swapping, a memory problem.
- `iostat -x`: `r_await/w_await` in ms vs device norms; `%util` near 100 for single devices (less meaningful for SSD/RAID arrays which parallelise).
- `free -m`: look at `available`, not `free`; low available + swapping = memory pressure.
- `sar -n TCP,ETCP`: `retrans/s` climbing = packet loss or overloaded remote.
- `dmesg`: `Out of memory: Killed process`, `nf_conntrack: table full`, `blk_update_request: I/O error`.

## Then
Apply the USE method per resource (utilisation, saturation, errors), then dig with `perf`, `bpftrace`/BCC tools (`biolatency`, `runqlat`, `tcpretrans`), or profiling. In containers, check cgroup throttling (`cat /sys/fs/cgroup/cpu.stat`: `nr_throttled`, `throttled_usec`).

## Verify
- [ ] Triage notes record each command's finding; the saturated resource identified matches the subsequent fix.
