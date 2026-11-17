---
id: computing-software.software-engineering.hpc-parallel-computing.io-benchmarks-ior-mdtest
name: io-benchmarks-ior-mdtest
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, ior, mdtest, io500, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Measuring I/O"
sources: ["https://ior.readthedocs.io/en/latest/userDoc/options.html", "https://ior.readthedocs.io/en/latest/userDoc/tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IOR and mdtest

Goal: benchmark storage.
- `mpirun -n 64 ior -a MPIIO -b 1g -t 4m -F` (file-per-process with `-F`) versus a single shared file (omit `-F`).
- Compare against expected hardware limits.
- Run when the system is quiet.
Verify: results documented per access pattern.

## Checked

2026-11-03. Confirmed against the official pages: IOR -a, -b, -t and -F options and file-per-process vs shared file (IOR options and tutorial pages). Removed: mdtest and its -n/-d options (mdtest page not read).

Method: documentation only; no commands were run.
