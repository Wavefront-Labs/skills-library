---
id: computing-software.web-development.frontend-development.browser-devtools-debugging-and-profiling
name: browser-devtools-debugging-and-profiling
category: computing-software
field: web-development
product: frontend-development
tags: [chrome-devtools, debugging, breakpoints, memory-leak, heap-snapshot, performance-panel, network-throttling, profiling, web-development, conditional-breakpoints, logpoints, network-panel]
level: advanced
status: docs-checked
description: "Chrome DevTools beyond console.log: conditional/DOM breakpoints, heap snapshot diffing for memory leaks, and reading the Performance panel."
sources:
  - https://developer.chrome.com/docs/devtools/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Browser DevTools — debugging and profiling beyond console.log

**Goal:** diagnose production-only bugs, memory leaks, and jank using the tools
built for it, instead of sprinkling `console.log` and guessing.

## 1. Breakpoints beyond "click the line number"
- **Conditional breakpoint**: right-click the line number, enter an expression —
  stops only when e.g. `items.length > 1000`, essential in a loop that runs
  thousands of times where you need the one bad iteration.
- **Logpoint**: same menu, logs an expression to console without pausing — faster
  than editing source to add a `console.log` and removing it after.
- **DOM breakpoint**: right-click an element → Break on → "subtree modifications"
  — pauses JS exactly when something changes a DOM node you didn't expect changed,
  without knowing which script did it.
- **XHR/fetch breakpoint** (Sources → bottom panel): pause whenever a request URL
  matching a pattern fires — useful for catching an unexpected duplicate call.
- **`debugger;` statement** in source is fine for local dev but never ships to
  production bundles — check it's stripped by the build; verify.

## 2. Network panel — throttling and waterfall reading
Throttle the network (a preset or a custom profile) before trusting any perceived-speed
assessment — fast wifi masks render-blocking resources and large payloads that
real users feel. In the waterfall, the "Queueing"/"Stalled" phase before a
request starts means the request was queued by the browser (the Network reference lists the reasons).
"Waiting (TTFB)" taking most of the bar means the backend is slow, not the
network — don't optimize frontend code for a server-side problem.

## 3. Memory leaks — heap snapshot diffing, not guessing
1. Take a heap snapshot (Memory panel) at a steady baseline.
2. Perform the suspected-leaky action several times (open/close a modal, navigate
   away and back) and force GC (the trash-can icon) before each snapshot.
3. Take another snapshot, select "Comparison" view against the baseline — objects
   with a growing count/retained size that should have been freed are the leak.
Common real causes: an event listener added on mount but never removed on
unmount, a `setInterval`/`setTimeout` not cleared, a closure captured by a global
cache (a map keyed by component instance that's never evicted), or a detached
DOM node still referenced by a JS variable (shows as "Detached HTMLDivElement" in
the snapshot — the classic leak signature).

## 4. Performance panel — reading a trace
Record while reproducing the jank. Look at: the **main thread flame chart** for
long yellow (scripting) blocks over 50ms (a "long task" that blocks input), the
**Summary** tab's breakdown (scripting vs rendering vs painting — tells you which
category to optimize), and **Layout Shift**/**LCP** markers overlaid on the
timeline matching Core Web Vitals. A repeated purple "Recalculate Style" +
"Layout" pattern inside a loop is layout thrashing — usually caused by reading a
layout-dependent property (for example `offsetHeight`) then writing
a style, then reading again, forcing synchronous reflow each iteration (batch
all reads before all writes).

## 5. Sourcemap-aware debugging in production
If error tracking (Sentry etc.) shows a minified stack trace with no readable
names, the uploaded source maps are missing or mismatched to that exact build —
verify the map matches the deployed bundle, not a stale previous build.

## Verify
- [ ] A suspected memory leak is confirmed via heap snapshot diff, not assumed from a growing task-manager number alone.
- [ ] Network waterfall is read with throttling on, and stalled/TTFB time is attributed correctly before blaming frontend code.
- [ ] Long tasks (>50ms) in a Performance trace are identified by name, not just "something is slow."
- [ ] Any `debugger;` statements are removed or confirmed stripped by the production build.
- [ ] Production source maps correspond to the exact deployed build hash.

## Checked

2026-11-02. Checked against Chrome DevTools docs (JavaScript breakpoints and reference, Network reference, Memory heap snapshots and memory problems, Performance reference) and web.dev pages on long tasks and layout thrashing: conditional breakpoints, logpoints, DOM subtree modifications breakpoints, XHR/fetch breakpoints, the debugger statement, Queueing/Stalled/Waiting (TTFB) timings, network throttling, heap snapshot Comparison view and the Detached filter, forcing garbage collection, 50 ms long tasks, scripting versus rendering colours, layout thrashing with offsetHeight. Removed because no fetched page states them: the Slow 3G preset name, the six-connections-per-origin and HTTP/2 explanation, getBoundingClientRect as a trigger, the claim that minifiers strip debugger, and the sourceMappingURL detail.

Method: documentation only; no commands were run.
