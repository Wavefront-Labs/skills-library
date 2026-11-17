---
id: computing-software.software-engineering.concurrency.controlling-the-benchmark-environment
name: controlling-the-benchmark-environment
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, benchmark-environment, cpu-frequency-scaling, cpu-isolation, turbo-boost, noise-reduction]
level: advanced
status: draft
description: "Reduce benchmark noise: fix CPU frequency and turbo, isolate cores, pin processes, control ASLR, background load and thermal effects, with pyperf system tune and cpupower."
sources: ["https://pyperf.readthedocs.io/en/latest/system.html", "https://llvm.org/docs/Benchmarking.html", "https://man.archlinux.org/man/cpupower.1", "https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling the benchmark environment

Goal: make run-to-run variance smaller than the effect you want to detect.

## CPU frequency and turbo
```
sudo cpupower frequency-set -g performance          # governor: avoid ramp-up delays
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo      # Intel: disable turbo
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost              # AMD/acpi-cpufreq: disable boost
sudo python -m pyperf system tune     # applies many of these; 'pyperf system reset' to undo
```
Turbo frequency depends on temperature and how many cores are busy, so results drift. Disabling it
lowers absolute speed but stabilises comparisons.

## Isolation
- Reserve cores: kernel params `isolcpus=2-3 nohz_full=2-3 rcu_nocbs=2-3` (reboot), or cgroup
  cpusets; move IRQs away (`/proc/irq/*/smp_affinity`).
- Pin the benchmark: `taskset -c 3 ./bench`, or `numactl --physcpubind=3 --membind=0`.
- Disable SMT siblings of benchmark cores (`echo off > /sys/devices/system/cpu/smt/control`) to avoid
  sharing execution units.
- Stop background services (indexers, browsers, cron, antivirus, update agents); don't benchmark on
  a laptop on battery.

## Other noise sources
- **ASLR** and memory layout can swing results several percent: `setarch $(uname -m) -R ./bench`
  to disable for a run, or randomise and average many runs (Stabilizer-style thinking).
- Environment size and working directory length shift stack alignment (Mytkowicz et al.,
  "Producing wrong data without doing anything obviously wrong").
- Thermal: let the machine reach steady state; watch `turbostat` for frequency/temperature.
- File system cache: drop caches (`echo 3 > /proc/sys/vm/drop_caches`) for cold runs or warm up for
  hot runs; be consistent.
- Cloud/VMs: noisy neighbours and CPU steal; use dedicated/bare-metal instances for serious work, or
  run A/B interleaved on the same instance many times.

## Record it
Store kernel, CPU model, governor, turbo state, isolation settings, compiler and flags alongside the
results; pyperf and BenchmarkDotNet capture much of this automatically.
