---
id: computing-software.software-engineering.javascript.js-heap-snapshot-analysis
name: js-heap-snapshot-analysis
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, heap-snapshot, js-memory]
level: advanced
status: docs-checked
description: "Find leaks with Chrome DevTools: Task Manager, memory recordings, detached-node heap snapshots and allocation timelines."
sources: ["https://developer.chrome.com/docs/devtools/memory-problems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap snapshots and allocation profiling

- Start with the Chrome Task Manager (Shift+Esc, or More tools > Task manager; enable the JavaScript memory column). The live number in parentheses is the memory used by reachable objects; if it keeps rising, objects are being created or growing.
- Performance panel: enable the Memory checkbox and record; start and end with a forced garbage collection (the Collect garbage mop button). A JS heap that ends higher than where it began after the forced GC, or a rising node count, can mean a leak.
- Heap snapshot: Memory panel, Heap Snapshot, Take snapshot, select it, then type `Detached` in the Class filter. A node is detached when it is removed from the DOM but JavaScript still references it; click a node and use the Objects pane to find the referencing variable, then remove that reference.
- Allocations on timeline: record while doing the suspect action; blue bars are new allocations and the candidates for leaks. Zoom on a bar to filter the Constructor pane to objects allocated in that time frame.
- Allocation sampling: shows memory allocation by function; the default view is Heavy (Bottom Up).
- Detached elements profile: shows the exact HTML nodes and the count of detached elements retained by JavaScript references.
- Frequent garbage collection shows as rapidly rising and falling Memory or JavaScript Memory values in the Task Manager, or JS heap and node count graphs in recordings; use an Allocation Timeline to find the allocating functions.
- There is no universal memory threshold; test on the devices your users have.

## Checked
2026-11-09. Rewritten from and confirmed against the Chrome for Developers page Fix memory problems (last updated 2024-11-06). Removed because the page does not state them: the Comparison view and Delta sort, the Retainers pane, shallow versus retained size definitions, `node --inspect` and `v8.writeHeapSnapshot()` for Node, the sawtooth baseline rule and the 10x self-check.
Method: documentation only; no commands were run.
