---
id: computing-software.cybersecurity-defensive.falco.troubleshoot-dropped-events
name: troubleshoot-dropped-events
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [buf-size-preset, cpus-for-each-buffer, dropped-events, kernel-drops, modern-ebpf]
level: advanced
status: docs-checked
description: "Reduce kernel-side syscall drops by tuning buf_size_preset, cpus_for_each_buffer, base_syscalls and rules, and read the drop metrics."
sources:
  - https://falco.org/docs/troubleshooting/dropping/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Action items when Falco drops syscall events on busy servers:
- Adjust `buf_size_preset` in `falco.yaml`.
- Use `base_syscalls` to limit monitored syscalls.
- Audit rules to avoid backpressure, because Falco's main event stream is single-threaded.
- Try running without plugins.

Falco allocates per-CPU buffers to move events from kernel to userspace. The size is fixed but adjustable; bigger buffers help with diminishing returns and preallocate more memory. Suggested starting values:
- `kmod` driver on large machines: `buf_size_preset` of `5` or `6`.
- `modern_ebpf` driver: `modern_ebpf.buf_size_preset` of `6` or `7` together with `modern_ebpf.cpus_for_each_buffer` of `4` or `6`, which shares larger buffers among several CPUs.

Measure drops by enabling `kernel_event_counters_enabled: true` and `libbpf_stats_enabled: true` in the metrics section; for `modern_ebpf` also enable `/proc/sys/kernel/bpf_stats_enabled`. Watch `scap.n_drops`, `scap.n_drops_perc`, `scap.evts_drop_rate_sec`, and the `scap.n_drops_buffer_*` categories. Falco 0.45 adds `scap.n_drops_auxmap_reentrancy` and `scap.n_drops_auxmap_pool_full` for the modern eBPF probe.

Normalise event rates by CPU count (`scap.evts_rate_sec` divided by `falco.host_num_cpus`). Adopter figures, with a grain of salt: under about 1.5K events per second per CPU is usually fine, over 3K is likely hard, and 1-2% drops on a few busy servers is considered acceptable.

Gotcha: moving all filtering into the kernel is not simple; kernel code runs in application context and can slow the application.

## Checked

2026-11-08. Read the cited dropping troubleshooting page in full and removed claims it does not support.

Method: documentation only; no commands were run.
