---
id: computing-software.qa-testing-engineering.performance-testing.nodejs-memory-leak-detection
name: nodejs-memory-leak-detection
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [node-memory-leak, dynamic-analysis, heap-snapshots, nodejs]
level: practitioner
status: docs-checked
description: "Detect Node.js memory leaks: watch the heap under load, take heap snapshots via the inspector, a signal or writeHeapSnapshot, and compare snapshots in DevTools."
sources:
  - https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot
  - https://jestjs.io/docs/cli
  - https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js memory leak detection

**Goal:** find what keeps memory growing in a Node service or test run.

## Confirm the leak
Run a steady load and log the process's heap usage periodically, or watch the container metric. Steady growth across GC cycles = leak.

## Heap snapshots
- Interactive: `node --inspect server.js`, connect Chrome DevTools, Memory tab, take snapshot.
- Headless: `node --heapsnapshot-signal=SIGUSR2 server.js`, then send that signal to the process; or call `require('node:v8').writeHeapSnapshot()` from a handler you do not expose publicly.

## Three-snapshot technique
1. Let the process finish bootstrapping and make the first allocations, snapshot 1.
2. Run N requests of the suspect operation, snapshot 2.
3. Run N more, snapshot 3.
4. In DevTools load the older file first, select the newer snapshot and switch **Summary** to **Comparison**, or use the Summary filter "Objects allocated between Snapshots 1 and Snapshots 2". Look for large positive deltas, and use the bottom panel to follow the references that hold them.

## Typical causes
Module-level caches/Maps without eviction, event listeners added per request, closures captured in timers/intervals never cleared, unbounded arrays of promises, global request-scoped data, large buffers held by streams not consumed.

## In test suites
Jest `--logHeapUsage` logs heap usage after every test (use with `--runInBand` and `--expose-gc` in node); `--detectOpenHandles` finds handles keeping the process alive.

## Gotchas
- A snapshot stops all other work on the main thread, can take over a minute, and is built in memory so it can double the heap; only take one in production from a process that can crash without hurting availability.
- Heap usage drops only after GC; run node with `--expose-gc` and force GC between samples for clean readings.

## Verify
Retainer path for the leaking objects is identified, and after the fix a repeat load shows a flat heap trend.

## Checked
2026-10-31. Confirmed on the Node.js Using Heap Snapshot page, the Chrome DevTools heap snapshots page and the Jest CLI page: the `--inspect` route, `--heapsnapshot-signal=SIGUSR2`, `require('node:v8').writeHeapSnapshot()`, the snapshot warning (main thread stops, can take over a minute, can double the heap), the two-snapshot Comparison method and the Summary filter "Objects allocated between Snapshots 1 and Snapshots 2", and `--logHeapUsage` / `--detectOpenHandles` / `--runInBand` / `--expose-gc`. Removed: the Clinic.js shortcut block and its source URL (the clinicjs.org docs page fetched as an empty shell, so `clinic doctor --autocannon`, `heapprofiler` and `bubbleprof` were unconfirmable this batch), `--heapsnapshot-near-heap-limit` (not on the fetched Node.js page), `process.memoryUsage().heapUsed` and `global.gc()`, the 15-30 min load duration and the autocannon/k6 tool names, the `-c 50 -d 120` autocannon arguments, `--detectLeaks`, `chrome://inspect`, and the `MaxListenersExceededWarning` hint.
Method: documentation only; no commands were run.
