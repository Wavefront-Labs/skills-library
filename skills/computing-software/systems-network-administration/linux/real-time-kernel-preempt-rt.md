---
id: computing-software.systems-network-administration.linux.real-time-kernel-preempt-rt
name: real-time-kernel-preempt-rt
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-rt, preempt-rt, realtime, cyclictest, rtla, latency, isolcpus, low-latency]
level: advanced
status: docs-checked
description: "Install and validate a real-time kernel (RHEL kernel-rt, Ubuntu Pro realtime, mainline PREEMPT_RT): tuned realtime profile, cyclictest/rtla tests, latency killers."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_for_real_time/9/html/optimizing_rhel_9_for_real_time_for_low_latency_operation/index
  - https://wiki.linuxfoundation.org/realtime/documentation/start
  - https://docs.kernel.org/tools/rtla/rtla-timerlat.html
  - https://docs.kernel.org/core-api/real-time/index.html
  - https://docs.kernel.org/tools/rtla/rtla-timerlat-top.html
  - https://docs.kernel.org/trace/hwlat_detector.html
  - https://github.com/redhat-performance/tuned/tree/master/profiles/realtime
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Real-time kernels (PREEMPT_RT)

**Goal:** bounded worst-case latency (tens of µs) for control systems, audio, telco/5G, trading — not
higher throughput (RT usually lowers throughput).

## Install
- Distribution packages: install the vendor's real-time kernel and its tuned profile; follow the vendor documentation for repositories and subscriptions.
- Build your own: `CONFIG_PREEMPT_RT=y` (see the kernel's real-time kernel-configuration documentation).
Check: `uname -v` contains `PREEMPT_RT`.

## Tune
```bash
echo "isolated_cores=2-7" >> /etc/tuned/realtime-variables.conf
tuned-adm profile realtime          # isolcpus, irqbalance banned CPUs and scheduler isolation for the isolated cores
reboot
```
Run the RT workload pinned to isolated cores with RT priority: `chrt -f 80 taskset -c 4 ./app`.
Firmware settings can add latency; use your hardware vendor's low-latency guidance.

## Measure
```bash
cyclictest ...                         # from rt-tests; the maximum latency is what matters (see its documentation for options)
rtla timerlat top -c 2-7 -d 1h        # -c CPUs to run sample threads on, -d session duration; reports IRQ and thread latency
# the hwlat tracer (ftrace) detects firmware/SMI-induced latency
```
Test under realistic load (stress-ng on housekeeping cores, network/disk traffic) for hours.

## Latency killers
SMIs and other firmware activity (detectable with the hwlat tracer), shared caches and memory bandwidth (see the kernel's real-time hardware documentation), IRQs on isolated cores.

## Verify
- [ ] cyclictest max under load is below your budget across a long run; `/proc/interrupts` shows no IRQs on isolated CPUs.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (core-api/real-time, trace/hwlat_detector, tools/rtla), `init/Makefile`, and the tuned `profiles/realtime` sources on 2026-10-26. Confirmed: `CONFIG_PREEMPT_RT` build option, `uname -v` contains PREEMPT_RT for such builds, tuned `realtime` profile with `isolated_cores` in realtime-variables.conf, rtla `timerlat top` with `-c` and `-d`, the hwlat tracer, shared cache/memory as latency sources. Removed: kernel version of the mainline merge (not stated in the documentation read), `/sys/kernel/realtime` (not found in the current kernel source), RHEL and Ubuntu install commands, cyclictest and hwlatdetect options, BIOS and latency-killer lists that no documentation covered.

Method: documentation only; no commands were run.
