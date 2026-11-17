---
id: computing-software.software-engineering.javascript.js-memory-leaks-and-garbage-collection
name: js-memory-leaks-and-garbage-collection
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-memory-leaks, garbage-collection, heap-snapshot, detached-dom]
level: advanced
status: draft
description: "Find and fix memory leaks in browser JavaScript using heap snapshots and allocation timelines."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Memory leaks

- GC frees what is unreachable from roots. Leaks are accidental reachability: forgotten timers (`setInterval` never cleared), listeners never removed (use `{ signal }` or `{ once: true }`), closures holding large objects, unbounded caches/Maps (use `WeakMap`/`WeakRef`, LRU, TTL), detached DOM nodes still referenced from JS, globals created by typos in sloppy mode.
- Find: DevTools Memory panel. Take a heap snapshot, do the action, force GC, take another, and use the "Objects allocated between Snapshot 1 and 2" view; sort by retained size; follow "Retainers". Use "Detached" in the class filter for orphaned DOM. The Performance panel's memory checkbox shows a sawtooth that never returns to baseline when leaking.
- `FinalizationRegistry` callbacks are not guaranteed to run; do not use them for correctness.
- Node: `node --inspect` and the same DevTools, `v8.writeHeapSnapshot()`, `process.memoryUsage()`.
- Confirm the fix by repeating the scenario 10-20 times and checking heap growth flattens.
