---
id: computing-software.systems-network-administration.restic.connections-and-concurrency
name: connections-and-concurrency
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, connections, concurrency, gomaxprocs, no-scan, read-concurrency]
level: advanced
status: docs-checked
description: "Tune restic backend connections, CPU use with GOMAXPROCS, file read concurrency, upfront scan and extra verification for slow or constrained hosts."
sources:
  - https://restic.readthedocs.io/en/stable/047_tuning_parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connections, CPU and concurrency

## Backend connections

Restic opens 5 connections per backend by default (2 for the local backend). Change with `-o <backend>.connections=N`:

```
restic -o rest.connections=5 backup /path/to/data
restic -o local.connections=2 backup /path/to/data
```

For high-latency backends it can help to raise the count, but this increases resource use and a too high count degrades performance; it can also lengthen uploads of temporary packs and increase SSD wear.

## CPU

Cap the cores used with `GOMAXPROCS=1`. The docs note that it may also slightly reduce memory use.

## File read concurrency

`--read-concurrency` on `backup` (or `RESTIC_READ_CONCURRENCY`) sets how many files are read in parallel. The docs say raising it can help when backing up from fast storage such as NVMe disks.

## Cut the upfront scan

`backup --no-scan` skips the initial pass that counts files and bytes. It saves extra I/O but removes the progress estimate.

## Skip extra verification

`backup --no-extra-verify` disables the check that generated files decode and hold the right data before upload. If you disable it, the docs say to verify the repository more actively with `restic check --read-data` (or `--read-data-subset`), because corruption from hardware issues or bugs might otherwise go unnoticed.

## Checked

2026-11-03. Confirmed in the restic docs page Tuning parameters: the global connection limit and `-o <backend>.connections`, defaults of 5 and 2 for local, the performance and wear warning, `GOMAXPROCS` and the memory note, `RESTIC_READ_CONCURRENCY`/`--read-concurrency`, `--no-scan` and its I/O trade-off, `--no-extra-verify` and the `check --read-data` advice. Removed: the spinning-disk advice and the closing nightly-job recipe (not in the docs).

Method: documentation only; no commands were run.
