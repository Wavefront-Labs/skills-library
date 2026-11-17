---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-troubleshoot-bpf-stats
name: tetragon-troubleshoot-bpf-stats
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [troubleshoot-bpf, tetragon, bpf-stats]
level: practitioner
status: docs-checked
description: "Measure Tetragon BPF program overhead with tetra debug progs and the overhead metrics, and enable BPF stats safely."
sources:
  - "https://tetragon.io/docs/troubleshooting/bpf-progs-stats/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon BPF program statistics

## BPF program statistics
Per-program run count and run time are shown in a top-like view or exported as metrics.

```shell
tetra debug progs          # Tetragon programs only
tetra debug progs --all    # all BPF programs
```
Columns: `Ovh` (system-wide overhead %), `Id` (global BPF ID, as in `bpftool prog`), `Cnt` (executions), `Time` (sum of execution time), `Pin` (bpffs pin path). Flags: `--once`, `--timeout N` (interval seconds, default 1), `--no-clear`, `--bpf-dir`, `--bpf-lib` (both auto-detected). Alias: `top`.

Metrics, labelled `namespace`, `policy`, `sensor`, `attach`: `tetragon_overhead_program_runs_total` and `tetragon_overhead_program_seconds_total`.

Stats are off by default because they add overhead. Enable with `sysctl kernel.bpf_stats_enabled=1` (set back to 0 when done) or run `tetra debug enable-stats`, which keeps them on only while the command runs (stop with Ctrl-C).

## Checked

2026-11-08. Read the BPF programs statistics page in full (raw docs markdown). Removed the log level and sysdump sections, the matching description text and two tags because the page does not cover them.

Method: documentation only; no commands were run.
