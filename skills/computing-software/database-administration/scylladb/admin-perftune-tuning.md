---
id: computing-software.database-administration.scylladb.admin-perftune-tuning
name: admin-perftune-tuning
category: computing-software
field: database-administration
product: scylladb
tags: [perftune, irq, cpu-mask, network-tuning, disk-tuning, performance]
level: advanced
status: docs-checked
description: "Seastar perftune.py: what it tunes (IRQ affinity, /proc/sys, disks, network), perftune.yaml and a consistent irq_cpu_mask, key options such as --tune, --nic, --dev, --dry-run."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/perftune.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# perftune.py

Seastar `perftune.py` tunes network and disk behaviour for maximum ScyllaDB performance: it reassigns IRQs to specific CPU cores so the remaining cores are free for ScyllaDB. It bans IRQs from irqbalance, sets parameters in `/proc/sys`, and distributes IRQs by SMP affinity according to `irq_cpu_mask` (large machines use more than one physical core). Persist tuning after reboot with a systemd unit that re-runs it at boot.

`perftune.yaml` is the output written with `--dump-options-file`. The `irq_cpu_mask` is determined on the first machine and written once (the file is generated only if absent). Use the same mask on all other machines, even ones added later, to avoid a mixed cluster.

Key options:
- `--tune net|disks|system`: components to tune (repeatable).
- `--nic <name>`: interface (default `eth0`, repeatable); `--num-rx-queues`; `--arfs` toggles aRFS.
- `--dev <device>` and `--dir <directory>`: disks or directories to optimise.
- `--cpu-mask` (cores to use, default all), `--irq-cpu-mask`, `--irq-core-auto-detection-ratio` (default 16: one IRQ core per 16 cores).
- `--get-cpu-mask`, `--get-cpu-mask-quiet`, `--get-irq-cpu-mask`: print masks.
- `--options-file`: read a YAML configuration.
- `--tune-clock`: also force `/system/clocksource` (default false, requires `--tune`).
- `--write-back-cache`: enable or disable write-back cache mode.
- `--dry-run`: print recommendations only; `--verbose` for detail.

```
perftune.py --tune net --nic eth0 --dry-run
```

## Checked

2026-11-04: what perftune.py does, the perftune.yaml behaviour and every listed option and default confirmed against the ScyllaDB perftune documentation page.

Method: documentation only; no commands were run.
