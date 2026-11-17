---
id: computing-software.qa-testing-engineering.test-case-design.memory-leak-detection-valgrind-heap
name: memory-leak-detection-valgrind-heap
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [dynamic-analysis, valgrind, heap-snapshot, memory-leak, memcheck, massif, tracemalloc, istqb-tta]
level: practitioner
status: docs-checked
description: "Detect memory leaks dynamically: Valgrind memcheck/massif for native code, tracemalloc for Python, heap dumps for JVM, and growth-under-repetition tests."
sources:
  - https://valgrind.org/docs/manual/mc-manual.html
  - https://valgrind.org/docs/manual/ms-manual.html
  - https://docs.python.org/3/library/tracemalloc.html
  - https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory leak detection

**Goal:** find memory that is allocated and never released, before it takes down production.

## Pattern: repetition test
Run the same operation N times (large enough to show a trend), force GC where possible, sample memory every K iterations. Steady growth with N = leak candidate; growth then plateau = cache warming.

## Native (C/C++)
```bash
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./app_tests
valgrind --tool=massif ./app && ms_print massif.out.<pid>   # heap over time (file name changeable with --massif-out-file)
```
"definitely lost" = real leak; "still reachable" blocks are still pointed to at exit and are often fine (globals). The leak summary reports both.

## Python
```python
import tracemalloc
tracemalloc.start(25)
s1 = tracemalloc.take_snapshot(); run_many(); s2 = tracemalloc.take_snapshot()
for stat in s2.compare_to(s1, "traceback")[:10]: print(stat)
```

## JVM
`jcmd <pid> GC.heap_dump filename=heap.hprof` (or the `-XX:+HeapDumpOnOutOfMemoryError` option), then analyse in a heap-dump tool such as Eclipse Memory Analyzer (MAT). Compare two dumps taken after a full GC.

## Node.js
`node --inspect`, heap snapshots in Chrome DevTools (Comparison view).

## Typical causes
Caches without eviction, listeners/callbacks never removed, static collections, unclosed resources, thread-locals in pools, closures capturing large objects.

## Gotchas
- Short tests don't show slow leaks; pair with soak tests.
- Measuring RSS alone misleads (allocator holds freed memory); use heap metrics.

## Verify
After the fix, the repetition test shows flat heap after warm-up across several sampling intervals.

## Checked
2026-10-31. Confirmed on the Valgrind Memcheck and Massif manuals: `--leak-check=full`, `--show-leak-kinds=all`, `--track-origins=yes`, `--tool=massif`, `ms_print massif.out.<pid>`, "definitely lost" and "still reachable". Confirmed on the Oracle Java 21 troubleshooting page: `jcmd <pid> GC.heap_dump filename=...` (the old form without `filename=` corrected), `-XX:+HeapDumpOnOutOfMemoryError`, Eclipse MAT named as an analysis tool. Python `tracemalloc.start(25)`, `take_snapshot`, `compare_to(..., "traceback")` match the tracemalloc docs and the snippet was run here on Python 3 and printed a size/count diff. Removed: the CTAL-TTA syllabus reference, the 1,000-100,000 iteration range, MAT dominator tree and leak suspects wording, the LeakSanitizer speed claim and the memlab pointer.
Method: documentation plus one local Python run of the tracemalloc snippet; valgrind was not run.
