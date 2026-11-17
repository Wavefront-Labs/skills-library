---
id: computing-software.software-engineering.hpc-parallel-computing.lustre-striping
name: lustre-striping
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, lfs-setstripe, lfs-getstripe, stripe-count, lustre, gpfs, burst-buffer, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Using Lustre well"
sources: ["https://doc.lustre.org/lustre_manual.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lustre striping and usage

Goal: tune I/O on Lustre.
- `lfs setstripe -c 8 dir` sets the stripe count for new files in a directory (default stripe count is 1, `-1` stripes over all OSTs); stripe size is set with `--size|-s` (default 1 MB, a multiple of 64 KB).
- Data on MDT (Lustre 2.11+) can place small files on the MDT.
- Many clients writing small chunks to one file suffer lock contention; aggregate writes or use MPI-IO collective writes.
Verify: I/O bandwidth scales with stripes in IOR.

## Checked

2026-11-03. Confirmed against the official pages: lfs setstripe synopsis, stripe count and size defaults, Data on MDT, small-chunk shared-file advice (Lustre manual). Removed: the -S short option, the 4m example, ls -l and node-local NVMe/burst-buffer advice.

Method: documentation only; no commands were run.
