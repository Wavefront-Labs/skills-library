---
id: computing-software.messaging-and-integration.redpanda.tuners-cpu-irq-disk-reference
name: tuners-cpu-irq-disk-reference
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [tuners, irq, cpu, disk-scheduler, ballast-file, thp, swappiness, fstrim]
level: advanced
status: docs-checked
description: "What each rpk redpanda tune tuner changes: cpu, disk_irq and net IRQ modes, disk scheduler, ballast file, fstrim, swappiness, THP, coredump, with redpanda.yaml keys and defaults."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-redpanda/rpk-redpanda-tune-list/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each tuner has a flag in `redpanda.yaml`, mostly `rpk.tune_<name>`. Defaults below are for production mode.

| Tuner | Effect | Key (prod default) |
|---|---|---|
| aio_events | Raises the max outstanding async I/O operations | `rpk.tune_aio_events` (true) |
| ballast_file | Creates a file you can delete to unblock a full disk | `rpk.tune_ballast_file` (true) |
| clocksource | Uses TSC via vDSO instead of the `xen` source | `rpk.tune_clocksource` (true) |
| coredump | Sets where coredumps are saved | `rpk.tune_coredump` (false) |
| cpu | `performance` governor; with reboot allowed also disables Intel P-states, C-states and turbo boost | `rpk.tune_cpu` (true) |
| disk_irq / net | Binds disk or NIC IRQs to chosen CPUs | `rpk.tune_disk_irq`, `rpk.tune_network` (true) |
| disk_nomerges | Disables merging of adjacent I/O requests | `rpk.tune_disk_nomerges` (true) |
| disk_scheduler | `none` for NVMe, `noop` otherwise | `rpk.tune_disk_scheduler` (true) |
| disk_write_cache | Write-through cache for GCP Local SSD only | `rpk.tune_disk_write_cache` (true) |
| fstrim | Background periodic trim service | `rpk.tune_fstrim` (true) |
| swappiness | Keeps process data in memory | `rpk.tune_swappiness` (true) |
| transparent_hugepages | Sets THP to `always` | `rpk.tune_transparent_hugepages` (false) |

**Ballast file.** Extra keys: `rpk.ballast_file_size` (default 1 GiB) and `rpk.ballast_file_path`. If the disk fills, delete the ballast to unblock failing writes, then stop the offender, delete topics or records and change retention.

**IRQ modes** (`--mode`): `sq` puts all IRQs of a device on CPU0, `sq_split` splits them between CPU0 and its HT siblings, `mq` spreads them over all CPUs. With no flag: NVMe-only gives `mq`; for non-NVMe, up to four HT siblings gives `mq`, else up to four cores gives `sq`, else `sq_split`.

**THP.** Redpanda already issues `madvise`, so the THP tuner only matters if the OS sets THP to `disabled`; hence off by default.

## Checked

2026-11-04. Every row, key, default, IRQ mode rule and the ballast and THP explanations were confirmed on the rpk redpanda tune list page (Tuners section).

Method: documentation only; no commands were run.
