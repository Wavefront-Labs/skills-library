---
id: computing-software.software-engineering.javascript.js-leak-patterns-listeners
name: js-leak-patterns-listeners
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, detached-dom-nodes, js-memory]
level: practitioner
status: docs-checked
description: "Recognise memory leaks, bloat and frequent GC, and find detached DOM trees with Chrome Task Manager, Performance recordings and heap snapshots."
sources: ["https://developer.chrome.com/docs/devtools/memory-problems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding leaks: detached DOM and growing heaps

- Symptoms: performance that gets progressively worse is possibly a memory leak (the page uses more and more memory); consistently bad performance is possibly memory bloat; frequent pauses are possibly frequent garbage collections (script execution pauses during collection). There is no hard "too much memory" number; test on devices your users have.
- A DOM node can be garbage collected only when nothing references it from the DOM tree or from JavaScript. A node removed from the tree but still referenced by JavaScript is detached, a common cause of leaks (the article's example keeps a detached `ul` in a variable `detachedTree`; the fix is to drop the reference when no longer needed).
- Chrome Task Manager (Shift+Esc, or More tools > Task manager; enable the JavaScript memory column): the Memory footprint column is OS memory where DOM nodes live, so a rising value means DOM nodes are being created. In JavaScript Memory, the live number (in parentheses) is memory used by reachable objects; if it rises, new objects are created or existing ones grow.
- Performance panel: enable the Memory checkbox and record; start and end with a forced garbage collection (Collect garbage button). A JS heap that ends higher than it began after the forced collection, or a rising node count, can mean a leak.
- Memory panel, Heap snapshot: take a snapshot and type `Detached` in the Class filter to find detached DOM trees; the Objects pane shows what references them. The Detached elements profile lists detached elements retained by JavaScript references.
- Allocations on timeline: record while performing the suspect action; blue bars are new allocations and candidates for leaks. Allocation sampling gives memory allocation by function.
- Frequently rising and falling memory values (Task Manager) or JS heap and node graphs (Performance) indicate frequent garbage collections.

Self-check: repeat the suspect action, force a garbage collection, and confirm the live JavaScript memory and node count return to the baseline.

## Checked

Confirmed on the Chrome DevTools "Fix memory problems" page (updated November 2024): symptoms, detached-node definition, Task Manager columns, Performance and Memory panel workflows. Removed: listener add/remove pairing and the `AbortController` `signal` tip, uncleared `setInterval`, `WeakMap`/`WeakRef`, LRU caches, closures, accidental globals and SPA teardown advice, and the "20 navigations" self-check, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
