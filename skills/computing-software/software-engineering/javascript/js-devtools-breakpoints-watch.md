---
id: computing-software.software-engineering.javascript.js-devtools-breakpoints-watch
name: js-devtools-breakpoints-watch
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, breakpoints, js-devtools]
level: practitioner
status: docs-checked
description: "Debug JavaScript in Chrome DevTools: event listener and line breakpoints, stepping, Scope, Watch and Console."
sources: ["https://developer.chrome.com/docs/devtools/javascript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breakpoints logpoints and call stacks

- The Sources panel has the Page tab (file tree), the Code Editor and the Debugger section (Scope, Watch, Breakpoints, Call stack and Event Listener Breakpoints).
- Breakpoints pause the code mid-execution and show all variable values at that moment, so you need not edit code and reload to add `console.log()` calls.
- Event Listener Breakpoints: expand a category (for example Mouse) and tick an event such as `click` to pause whenever a listener for it runs. A browser extension's own listener may pause first; Incognito Mode disables extensions.
- Line-of-code breakpoint: click the line number in the gutter; execution pauses before that line, and values are shown inline next to earlier declarations.
- Step into next function call and Step over next function call walk execution one line at a time; Resume continues to the next breakpoint.
- Scope tab: local, global and closure variables while paused (double-click a value to edit). Watch tab: add any valid JavaScript expression, for example `typeof sum`, to monitor it over time. The Console drawer (Escape) evaluates expressions in the paused scope.
- Other breakpoint types the tutorial names: conditional breakpoints (trigger only when your condition is true), breakpoints on caught or uncaught exceptions, and XHR breakpoints (trigger when the requested URL matches a substring).
- Edits made in DevTools only change the code running in your browser; Workspaces can save edited files to your sources. Deactivate breakpoints ignores all breakpoints. From Chrome 105 you can edit a paused function live.

Self-check: add a Watch expression such as `typeof x` while paused and confirm it updates on each step.

## Checked
2026-11-09. Rewritten from and confirmed against the Chrome for Developers page Debug JavaScript (last updated 2024-05-22). Removed because the page does not state them: logpoints, DOM breakpoints, async call stacks, keyboard shortcuts for stepping, the ignore list, `debugger;` and ESLint `no-debugger` advice, Local Overrides, and the `console.table`/`time`/`trace`/`copy` helpers.
Method: documentation only; no commands were run.
