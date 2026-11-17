---
id: computing-software.cybersecurity-defensive.falco.falco-performance-monitoring
name: falco-performance-monitoring
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [performance, resource-utilization, cpu-rss, hot-path, event-drops]
level: intro
status: docs-checked
description: "Monitor Falco CPU, memory and drop metrics in production, and know that its single-threaded hot path caps at one CPU."
sources:
  - https://falco.org/docs/troubleshooting/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco's health has several dimensions: resource use and system impact, upgrades and restarts, data quality, end-to-end alert delivery, and security coverage including resilience to bypass.

Set resource limits for your deployment, since a kernel tool can slow the kernel or request rates of applications. Check that applications behave as before, looking at network, I/O and contention.

Top resource metrics:
- CPU usage as a percentage of one CPU. Falco's hot path is single-threaded, so it cannot exceed one full CPU.
- Memory RSS, the part of memory held in RAM.
- Memory VSZ, the total allocated including swap.
- `container_memory_working_set_bytes` on Kubernetes, nearly equal to the cgroups `memory_used` metric exposed by Falco metrics.

Falco's utilisation is not constant. It follows the host workload: the more syscalls applications make, the more work Falco does. Top load metrics:
- Kernel-side and userspace event counts.
- Kernel-side and userspace drop counts.
- Kernel tracepoint invocation counts, to deduce server load.
- Userspace timeouts.
- Internal state counters.

Falco has native support for these counters (see its Metrics guide), and the dropped events troubleshooting guide applies when drop counts rise.

Gotcha: utilisation tracks syscall volume, so do not size limits from an idle host.

## Checked

2026-11-08. Read the Performance page in full. Removed the unsupported instruction to enable the metrics section; reworded the sizing gotcha.

Method: documentation only; no commands were run.
