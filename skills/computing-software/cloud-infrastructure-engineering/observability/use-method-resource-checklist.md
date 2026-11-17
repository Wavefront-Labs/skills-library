---
id: computing-software.cloud-infrastructure-engineering.observability.use-method-resource-checklist
name: use-method-resource-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [use-method-checklist, resource-utilization-saturation-errors, use-method, node-exporter, linux, saturation-metrics]
level: practitioner
status: docs-checked
description: "Apply Brendan Gregg's USE method per resource (CPU, memory, storage, network, software) with Linux tool checks and the matching node_exporter collectors."
sources: ["https://www.brendangregg.com/usemethod.html", "https://github.com/prometheus/node_exporter", "https://www.brendangregg.com/USEmethod/use-linux.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USE method checklist

For every resource, check utilization, saturation and errors. Start from questions, not available metrics; mark unavailable metrics as unknown.

## Definitions (Gregg)
- Utilization: average time the resource was busy servicing work, as a percentage over an interval.
- Saturation: work the resource cannot yet service, typically queue length or wait time. Any nonzero value can indicate a problem.
- Errors: counts of error events, including recoverable failures and retries.

## Procedure
1. Build a resource list or block diagram.
2. For each resource, find the utilization, saturation and error metric, with the tool that reads it.
3. Check errors first (quick to interpret), then utilization and saturation. Investigate findings with other methods and iterate.
4. 100 % utilization usually means a bottleneck; above roughly 70 % can already hurt (long averages hide bursts; disks cannot be preempted). Long sampling intervals can hide saturation.

## Linux checks (Gregg's Linux checklist)
| Resource | Utilization | Saturation | Errors |
|---|---|---|---|
| CPU | vmstat 1 (us, sy, st), mpstat -P ALL 1, sar -u | vmstat r compared with CPU count, sar -q runq-sz | perf processor error events if available |
| Memory | free -m, vmstat, sar -r | vmstat si/so (swapping), sar -B pgscan, OOM kills in dmesg | dmesg for hardware failures |
| Network | sar -n DEV 1, ip -s link, nicstat | ifconfig overruns/dropped, netstat -s retransmits, sar -n EDEV | netstat -i RX-ERR/TX-ERR, ip -s link errors |
| Storage I/O | iostat -xz 1 %util, sar -d | iostat avgqu-sz above 1 or high await | smartctl, ioerr_cnt in sysfs |
| Storage capacity | df -h, swapon -s | none given (a full disk returns ENOSPC) | strace for ENOSPC |
| File descriptors | sar -v file-nr vs file-max; /proc/PID/fd vs ulimit -n | questionable (no queueing) | strace for EMFILE |
| Task capacity | top Tasks vs threads-max | threads blocked on memory allocation | fork or pthread_create failures |

Software resources such as mutexes, thread pools, process limits and file descriptors can be included where the metrics are useful; hardware caches are generally excluded. In cloud environments, hypervisor or cgroup limits can be treated as resources.

## node_exporter
Default collectors include cpu, loadavg, meminfo, vmstat, diskstats, filesystem, netdev, netstat, sockstat, and pressure (PSI, needs kernel 4.20+ or CONFIG_PSI). Disabled by default (opt in one at a time, watching scrape_duration_seconds) are cgroups, interrupts, softirqs, processes, systemd, perf, swap and others. The textfile collector reads *.prom files for machine-specific metrics.

## Gotcha
%util near 100 % does not tell you a modern multi-queue device is saturated; look at queue depth and latency (general knowledge, not on the cited pages).

## Verify
- [ ] Each resource has a utilization, saturation and error check, or a recorded unknown
- [ ] Software resources you own export in-use, max and wait values

## Checked

2026-11-08. Confirmed on the three pages: USE definitions, procedure, 70 % guidance, resource scope, cloud note, the Linux checklist rows above, and node_exporter default/disabled collector lists, PSI requirement and textfile collector. Removed: all PromQL expressions with specific node_* metric names (the node_exporter README lists collectors, not metric names), container throttling formula, and the "18 cells" count. The %util gotcha is flagged as general knowledge.
Method: documentation only; no commands were run.
