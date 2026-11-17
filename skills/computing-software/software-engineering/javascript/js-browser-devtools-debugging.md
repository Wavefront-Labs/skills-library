---
id: computing-software.software-engineering.javascript.js-browser-devtools-debugging
name: js-browser-devtools-debugging
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-devtools, breakpoints, console-debugging, source-maps, performance-panel]
level: practitioner
status: draft
description: "Debug JavaScript in browser DevTools with breakpoints, logpoints, source maps and the Performance panel."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser DevTools debugging

- Sources panel: line breakpoints, conditional breakpoints, logpoints (log without editing code), `debugger;` statement, DOM/XHR/event-listener breakpoints, "Pause on exceptions" (uncaught/caught), blackbox third-party scripts.
- Inspect: scope panel, watch expressions, call stack with async stack traces, `$0` (selected element), `$_`, `copy(obj)`, `console.table`, `console.group`, `console.time`, `console.trace`, `monitorEvents(el)`, `getEventListeners(el)`.
- Source maps: ship `.map` files (or `sourceMappingURL`) and enable them in DevTools to debug original TypeScript; check "Enable JavaScript source maps".
- Network panel: throttling, "Disable cache", copy as fetch/cURL; Application panel for storage and service workers.
- Performance panel: record, find long tasks (red corner), flame chart, "Bottom-Up" by self time; Lighthouse for audits.
- Reproduce, bisect with breakpoints, read the first error not the last.
