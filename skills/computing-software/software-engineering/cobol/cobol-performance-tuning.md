---
id: computing-software.software-engineering.cobol.cobol-performance-tuning
name: cobol-performance-tuning
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cobol-performance-tuning, cobol-performance, performance-tuning, blocksize-0, comp-vs-display, bufno]
level: advanced
status: draft
description: "Speed up batch COBOL: pick USAGE for hot arithmetic, tune blocking and buffering, and avoid linear searches in loops."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Numeric USAGE, I/O blocking and table search performance
**Goal:** measurable gains with low risk.

- Arithmetic: binary (COMP) subscripts and counters; packed decimal for decimal money; avoid DISPLAY arithmetic and COMP-3 with an odd digit count (alignment) in hot paths; use `OPT(2)` and `ARITH(COMPAT)` only if the range suffices.
- Subscripts: use indexes for table search; avoid recomputation inside loops.
- Tables: SEARCH ALL on sorted tables; preload lookup data once instead of file or SQL calls per record.
- Files: `BLOCK CONTAINS 0` for system-determined blocksize; `BUFNO` in the DD for sequential throughput; avoid OPEN/CLOSE per record; sort instead of random access when volumes are high.
- DB2: avoid per-row SELECTs in loops, use multi-row FETCH/INSERT, commit in batches.
- Measure first: use SMF/RMF timings, `EXEC` CPU times in the job log, or a profiler such as IBM Application Performance Analyzer; for GnuCOBOL use `perf`/`gprof` on the executable.

## Gotchas
- Optimizing without a baseline wastes time; compare CPU and elapsed on the same data volume.
- TRUNC(OPT) can change results at boundaries (see precision skill).

## Self-check
Record before/after CPU seconds for a 1-million-record run.
