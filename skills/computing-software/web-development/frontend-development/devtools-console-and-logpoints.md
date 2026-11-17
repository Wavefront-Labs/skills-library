---
id: computing-software.web-development.frontend-development.devtools-console-and-logpoints
name: devtools-console-and-logpoints
category: computing-software
field: web-development
product: frontend-development
tags: [console-api, logpoints, devtools-console-utilities, debugging, chrome-devtools]
level: practitioner
status: docs-checked
description: "Getting more from the Chrome DevTools console: console.table/group/time/count, logpoints without code edits, and $0/$$/copy/monitorEvents utilities."
sources:
  - https://developer.chrome.com/docs/devtools/console/api
  - https://developer.chrome.com/docs/devtools/console/utilities
  - https://developer.chrome.com/docs/devtools/javascript/breakpoints#log
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevTools console and logpoints

## 1. Console API beyond log
```js
console.table(rows, ["id", "status"]);       // array of objects as a table; optional column subset
console.group("checkout"); console.info("step 1"); console.groupEnd("checkout");
console.time("render"); render(); console.timeEnd("render");
console.count("effect run");                 // times count() was called at this line with this label
console.assert(total >= 0, { total });       // logs an error only when the expression is false
console.trace();                             // prints a stack trace
console.dir(element);                        // JSON-style representation of the object
```
- `console.groupCollapsed(label)` starts a group collapsed; groups can be nested.
- `console.countReset([label])` resets a count.
- Most `console.*` methods have a severity level (assert and error: Error; warn: Warning; debug: Verbose; log, info, table, dir, count, trace: Info) which the Console can filter on.
- Right-click a logged table to copy it as Markdown or CSV.
- `console.clear()` is disabled while Preserve Log is on.

## 2. Logpoints
Sources panel > right-click a line number > **Add logpoint** > enter the message or expressions. It logs to the Console without pausing and without adding `console.log()` calls to your code (a pink icon with two dots marks the line). A conditional breakpoint whose condition evaluates to false is the older way to get the same effect, and a "Never pause here" breakpoint is just a conditional breakpoint with a false condition.

## 3. Console utilities (Console only)
These work only when called from the DevTools Console, not from your scripts.

| Utility | Does |
|---|---|
| `$0` to `$4` | the last five elements inspected in the Elements panel (or heap objects selected in Profiles); `$0` is the most recent |
| `$(sel)`, `$$(sel)` | `document.querySelector` and `Array.from(document.querySelectorAll())` shortcuts, with an optional start node; overwritten if a library such as jQuery defines `$` |
| `$x(path)` | elements matching an XPath expression |
| `$_` | value of the most recently evaluated expression |
| `copy(x)` | copy a string representation of x to the clipboard |
| `monitorEvents(window, ["resize", "scroll"])` | log events on an object; `unmonitorEvents` stops; event types such as `"key"` or `"mouse"` map to predefined sets |
| `getEventListeners(obj)` | listeners registered on an object, by event type |
| `queryObjects(Constructor)` | objects created with that constructor, in the selected execution context |
| `debug(fn)` / `undebug(fn)` | break inside fn when it is called |
| `monitor(fn)` / `unmonitor(fn)` | log fn's name and arguments on each call |
| `keys(obj)`, `values(obj)` | property names, property values |
| `profile(name)` / `profileEnd(name)` | start and stop a CPU profile; results open in Performance |

## Verify
- [ ] You can answer "how many times did this run per click" with `console.count` or a logpoint, without a rebuild.

## Checked

2026-11-09. Read in full the Console API reference and Console Utilities API reference, and the logpoint and conditional breakpoint sections of the breakpoints page. Confirmed the method behaviours, log levels, utility behaviours, Preserve Log note and logpoint steps. Removed: the live-reference and structuredClone advice, the `%c` styling example, the live expressions section, the filter syntax list, the production-stripping gotchas and the iframe context note, which these pages do not state.

Method: documentation only; no commands were run.
