---
id: computing-software.software-engineering.debugging.managed-runtime-memory-leaks
name: managed-runtime-memory-leaks
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, memory-debugging, memory-leaks, heap-snapshot, managed-memory-leak, chrome-devtools-memory, tracemalloc, retainers, gc-roots, python-memory-leak, node-memory-leak]
level: advanced
status: docs-checked
description: "Find leaks in garbage-collected runtimes (Node/browser JS, .NET, Python, JVM) by comparing heap snapshots and following retainer paths to the GC root."
sources: ["https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak", "https://docs.python.org/3/library/tracemalloc.html", "https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Managed-runtime memory leaks

**Goal:** in a GC language, a leak is an object that is still REACHABLE but no longer
needed. Find what keeps it reachable.

## Method (same for every runtime)
1. Confirm the growth is real (growth in memory usage over time) before collecting heavy data.
2. Take a snapshot after warm-up, run the suspect operation, take another.
3. Compare: an action and its reverse (open a document, close it) should not leave extra objects behind.
4. Pick one leaked instance and find how and why it is rooted; the first holder in that chain that
   should not keep it is the bug.

## Node.js / browser
- Chrome DevTools heap snapshots show only objects reachable from the global object, and taking a snapshot
  always starts with garbage collection.
- Views: **Summary** (objects grouped by constructor, with shallow and retained sizes; a filter finds
  objects retained by detached DOM nodes) and **Comparison** (differences between snapshots, to confirm a
  leak by inspecting the delta). The number after `@` is an object's unique ID, for per-object comparison.
- Node.js: attach DevTools via `--inspect`, or write snapshots from a signal:
```bash
node --heapsnapshot-signal=SIGUSR2 index.js
```
  Load the snapshots in DevTools, select the newer one and switch Summary to Comparison.

## .NET
Per the Microsoft guide: check managed memory with `dotnet-counters`, then collect and analyse a dump.
```bash
dotnet-counters monitor --refresh-interval 1 -p <pid>      # watch the System.Runtime counters
dotnet-dump collect -p <pid>
dotnet-dump analyze <dump-file>
> dumpheap -stat               # object counts by type
> dumpheap -mt <MT>            # instances of one method table
> gcroot <address>             # how and why the object is rooted
```

## Python
`tracemalloc` compares allocation snapshots:
```python
import tracemalloc
tracemalloc.start(25)          # store up to 25 frames per allocation
snapshot1 = tracemalloc.take_snapshot()
# ... run the suspect workload ...
snapshot2 = tracemalloc.take_snapshot()
for stat in snapshot2.compare_to(snapshot1, "traceback")[:10]:
    print(stat)
```
Storing more than 1 frame is only useful for statistics grouped by `'traceback'` or cumulative statistics.
To trace most allocations, start it early with `PYTHONTRACEMALLOC=1` or `-X tracemalloc`. It traces Python
allocations only.

## JVM
Heap dumps + Eclipse MAT dominator tree and path-to-GC-roots (see
computing-software.software-engineering.java.heap-dump-and-memory-leak-analysis).

## Verify
- [ ] After the fix, snapshot comparison over repeated runs shows no per-run growth.
- [ ] A soak test keeps post-GC heap flat.

## Checked
2026-11-09. Confirmed against Chrome DevTools "Heap snapshots" (reachability, Summary and Comparison views,
detached nodes), the Node.js "Using heap snapshot" guide (`--heapsnapshot-signal`, Comparison), Microsoft
"Debug a memory leak in .NET" (dotnet-counters, dotnet-dump, dumpheap, gcroot) and the Python tracemalloc
docs (start, take_snapshot, compare_to, nframe, PYTHONTRACEMALLOC). Removed as not stated in these pages:
dotnet-gcdump and PerfView, the causes lists for each runtime, objgraph and gc.get_referrers advice, and
the `kill -USR2` shortcut.
Method: documentation only; no commands were run.
