---
id: computing-software.web-development.web-performance.script-parse-compile-and-evaluation-cost
name: script-parse-compile-and-evaluation-cost
category: computing-software
field: web-development
product: web-performance
tags: [parse-compile-cost, script-evaluation, javascript-performance, main-thread, code-caching]
level: advanced
status: docs-checked
description: "JavaScript parse, compile and evaluation cost: V8 streaming and code caching, splitting bundles, JSON.parse for big data, and reducing startup main-thread work."
sources:
  - https://v8.dev/blog/cost-of-javascript-2019
  - https://v8.dev/blog/code-caching-for-devs
  - https://web.dev/articles/script-evaluation-and-long-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Script evaluation, parse and compile cost

V8's 2019 article says parse and compile are no longer as slow as once thought: the dominant costs of processing scripts are now download time and CPU execution time. A busy main thread delays user interaction, and some parse and compile work still happens on the main thread. Not every engine implements script streaming.

## 1. How V8 helps
- **Streaming**: scripts are streaming-parsed and compiled on a worker thread; V8 starts streaming once it has seen at least 30 kB (Chrome 72 onward also streams regular synchronous scripts, but not inline scripts). V8 reports an average 40% cut in main-thread parse and compile work from this.
- **Wrapped bundles hurt**: the article notes that large bundles wrapped in outer functions cause lots of lazy compilation on the main thread, and suggests splitting large bundles into smaller ones (for example 50 kB each, unwrapped) to parallelise streaming.
- **Code caching** (V8 and the code-caching article): cached after execution, so only functions compiled by the time the script finishes executing are included; event handlers, promise chains and unused library functions stay lazy. Chrome caches the compiled code when the first two visits are within 72 hours; with a service worker cache it caches eagerly. Scripts under 1 KiB are not code-cached, so avoid inlining non-trivial scripts into the HTML.
- **Cache invalidation**: a 200 response with changed content clears the code cache; a 304 keeps it. Code in a separate library file keeps its cache across changes to your own code, and is shared across pages that load it.
- **IIFE hint**: wrapping a function in parentheses makes engines compile it immediately, which can force it into the code cache, but the article advises avoiding that unless necessary.

## 2. Reduce it
1. Keep bundles small, especially for mobile; if a bundle exceeds about 50-100 kB, split it (with HTTP/2 multiplexing the extra requests cost less).
2. Avoid long tasks; break them up. web.dev says to break up script evaluation by splitting loaded code into multiple smaller scripts rather than a few large ones.
3. Avoid large inline scripts, which are parsed and compiled on the main thread (rule of thumb: over 1 kB, do not inline).
4. For objects of 10 kB or more, `JSON.parse('...')` of a string is cheaper than an equivalent JavaScript object literal (V8 measured 1.7 times faster; it is also not at risk of being parsed twice), provided the string is evaluated only once. Measure before changing.
5. Scripts requested by a Web Worker are evaluated off the main thread (web.dev).

## 3. Verify with tools
The code-caching article says DevTools does not expose code cache information; use `chrome://tracing` with the `v8` category to see whether scripts are cached.

## Verify
- [ ] Startup Performance trace shows no long tasks from script evaluation, and (via chrome://tracing) library bundles are consumed from the code cache on repeat visits.

## Checked
2026-11-09. Read "The cost of JavaScript in 2019" and "Code caching for web developers" (searched for the cited figures and rules; not every section read) and web.dev "Script evaluation and long tasks" (searched, not read end to end). Removed (not on those pages): the 200 KB device-cost claim, DevTools event names, Lighthouse audit names, the Long Animation Frames fields, `scheduler.yield` and `postTask` advice, `requestIdleCallback` deferral, the 500 ms and 50 ms verification targets, and the DevTools performance reference source (not fetched).
Method: documentation only; no commands were run.
