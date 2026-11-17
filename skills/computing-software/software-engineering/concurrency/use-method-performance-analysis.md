---
id: computing-software.software-engineering.concurrency.use-method-performance-analysis
name: use-method-performance-analysis
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, profiling, performance, use-method, utilization-saturation-errors, red-method, bottleneck-analysis, systems-performance, linux-perf-tools]
level: advanced
status: docs-checked
description: "Find system bottlenecks fast with Brendan Gregg's USE method (utilization, saturation, errors per resource) and the Linux commands for each resource."
sources: ["https://www.brendangregg.com/usemethod.html", "https://www.brendangregg.com/USEmethod/use-linux.html", "https://grafana.com/blog/the-red-method-how-to-instrument-your-services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The USE method

**Goal:** a checklist that finds systemic resource bottlenecks early in an investigation, instead of starting from given metrics and working backwards. Gregg: it solves about 80% of server issues with 5% of the effort, but it is one tool in a larger toolbox and does not solve many problem types.

## Method
For every resource, check:
- **Utilization**: the percentage of time the resource was busy (at 100% no more work can be accepted).
- **Saturation**: the degree to which the resource has extra work it cannot service, often queued (for example run-queue length).
- **Errors**: the count of error events.
Resources: CPUs, memory, network interfaces, storage devices and controllers, interconnects (CPU, memory, I/O), plus software resources (mutex locks, thread pools, file descriptor capacity). Hardware caches are left out: caches improve performance under high utilization, so check hit rates after systemic bottlenecks are ruled out.
- Investigate errors: recoverable failures (retried operations, one device in a redundant pool failing) degrade performance without being noticed.
- The first problem found may be a problem rather than the problem; continue iterating over the remaining resources.
- Start with the easy metrics, which find the most common issues: CPU saturation, memory capacity saturation, network interface utilization, disk utilization.

## Linux checklist (from Gregg's Linux USE page)
| Resource | Utilization | Saturation | Errors |
|---|---|---|---|
| CPU | `vmstat 1` us+sy+st; `mpstat -P ALL 1` per CPU; `top` per process | `vmstat 1` "r" > CPU count; `sar -q` runq-sz; `perf sched latency` | `perf` processor-specific error events if available |
| Memory | `free -m`, `vmstat 1`, `sar -r` | `vmstat 1` si/so (swapping); `sar -B` pgscan; OOM killer in `dmesg` | `dmesg` for physical failures |
| Network | `sar -n DEV 1`, `ip -s link` vs max bandwidth | `netstat -s` retransmits, `ifconfig` overruns/dropped, `sar -n EDEV` | `netstat -i` RX-ERR/TX-ERR, `ip -s link` errors |
| Disk I/O | `iostat -xz 1` %util | `iostat -xnz 1` avgqu-sz > 1 or high await | `smartctl`, `/sys/devices/.../ioerr_cnt` |
| File descriptors | `ls /proc/PID/fd` count vs `ulimit -n`; `sar -v` file-nr | Gregg: no obvious queueing | `strace` for EMFILE |
Notes from that page: `vmstat` "r" on recent Linux counts both waiting and running threads; Linux load averages include uninterruptible (often I/O) tasks so they are not used as a CPU metric; dropped packets count as both saturation and errors; a single hot CPU can mean a single hot thread or a mapped hardware interrupt.
Software resources: for a mutex, utilization is time held and saturation is threads queued waiting; for a thread pool, utilization is time threads were busy and saturation is requests waiting to be serviced.

## Interpreting
- Low utilization averaged over a long interval can hide bursts: Gregg's example had 100% CPU for seconds inside five-minute averages while latency suffered, so use short intervals.
- Low utilization, no saturation, no errors is a useful result: it narrows the scope of the investigation.

## USE vs RED
Per Tom Wilkie (Grafana Labs), USE applies to hardware resources (network, disks) and is somewhat abstract for memory; for microservices he created RED per service: Rate (requests per second), Errors (failing requests), Duration (time requests take). RED is a good proxy for how happy customers are and for alerts and SLA measurement.

## Verify
- [ ] Each resource checked for utilization, saturation and errors, with the saturated one identified from numbers.
- [ ] Dashboards include saturation metrics, not just utilization.

## Checked
2026-11-08. Confirmed against Brendan Gregg's USE Method page and Linux USE checklist and the Grafana RED Method post. Removed (not on those pages): `runqlat`, `ss -tm`, `nstat`, Pressure Stall Information and its kernel version, cgroup CPU throttling (`cpu.stat`, `container_cpu_cfs_throttled_seconds_total`), the "errors first" ordering and the app-pool metric rows. The Systems Performance book reference was not used.
Method: documentation only; no commands were run.
