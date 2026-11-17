---
id: computing-software.web-development.frontend-development.closures-and-lexical-scope
name: closures-and-lexical-scope
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-classes, closures, lexical-scope, javascript, memory-leaks]
level: practitioner
status: docs-checked
description: "Using closures and lexical scope deliberately: private state, factories, let vs var in loops, stale closures in React hooks, and closure-driven memory leaks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let
  - https://react.dev/learn/removing-effect-dependencies
  - https://react.dev/learn/state-as-a-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures and lexical scope

A closure is a function plus the variables in scope where it was **created**. Scope is lexical: decided by where code is written.

## 1. Private state and factories
```js
function createCounter(start = 0) {
  let n = start;                         // not reachable from outside
  return { inc: () => ++n, get value() { return n; } };
}
const once = fn => { let done = false, r; return (...a) => done ? r : (done = true, r = fn(...a)); };
```

## 2. Loops: let vs var
```js
for (var i = 0; i < 3; i++) setTimeout(() => console.log(i));  // 3 3 3 - one shared binding
for (let i = 0; i < 3; i++) setTimeout(() => console.log(i));  // 0 1 2 - fresh binding per iteration
```
`const`/`let` are block-scoped and in the temporal dead zone until declared (`ReferenceError` if read early); `var` is function-scoped and hoisted as `undefined`.

## 3. Stale closures
A callback captures the variable binding from its render/creation. In React:
```js
useEffect(() => { const id = setInterval(() => setCount(count + 1), 1000); return () => clearInterval(id); }, []);
// count is frozen at its first value -> stops at 1
```
Fix: functional update `setCount(c => c + 1)`, list the dependency, or read from a ref. The same bug occurs with event listeners registered once and reading outer variables that later get reassigned.

## 4. Memory
A closure keeps the variables it references alive for as long as the function itself is reachable. MDN also advises against creating functions inside other functions when closures are not needed, because each function instance manages its own scope and closure.
- Remove listeners/intervals that close over big data (`AbortController`, `clearInterval`).
- Do not cache closures in module-level Maps keyed by request without eviction.

## 5. Module scope
ES modules give each file its own scope - a top-level `let` is module-private and a singleton for the page/process. Server-side that singleton is shared across all requests: never store per-user data there.

## Verify
- Heap snapshot: find the retained object and follow its retainers back to the function that holds it.
- Unit tests for factory isolation: two counters do not share state.

## Checked

2026-10-26. MDN JavaScript Closures guide, `let` reference (temporal dead zone raises `ReferenceError`; `var` is function-scoped) and react.dev (updater functions replace reads of state inside effects; state is a snapshot per render) read from their source repositories. Removed the unconfirmed claim that sibling closures share one context object and the DevTools retainer label.

Method: documentation only; no commands were run.
