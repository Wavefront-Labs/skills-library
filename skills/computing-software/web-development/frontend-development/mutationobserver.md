---
id: computing-software.web-development.frontend-development.mutationobserver
name: mutationobserver
category: computing-software
field: web-development
product: frontend-development
tags: [dom-manipulation, mutationobserver, dom, observers, javascript]
level: practitioner
status: docs-checked
description: "Watching DOM changes with MutationObserver: choosing childList/attributes/subtree options, batching records, avoiding feedback loops and performance pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver
  - https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/observe
  - https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MutationObserver

## 1. Use cases
Reacting to DOM you do not control: third-party widgets, CMS content, browser extensions, enhancing elements as they appear, test utilities. If you own the code that changes the DOM, call your function directly instead.

## 2. Pattern
```js
const mo = new MutationObserver(records => {
  for (const r of records) {
    if (r.type === "childList") r.addedNodes.forEach(n => n.nodeType === 1 && enhance(n));
    if (r.type === "attributes") onAttr(r.target, r.attributeName, r.oldValue);
  }
});
mo.observe(container, {
  childList: true, subtree: true,
  attributes: true, attributeFilter: ["data-state", "aria-expanded"], attributeOldValue: true,
});
// later: mo.disconnect();   mo.takeRecords() to flush pending
```
At least one of `childList`, `attributes`, `characterData` must be true or `observe()` throws a `TypeError`.

## 3. Semantics
- Callbacks are delivered as a **microtask** after the mutating script - batched, async, before rendering.
- `addedNodes` contains only the inserted subtree roots - query inside them (`n.querySelectorAll(".widget")`) for descendants.

## 4. Pitfalls
- **Feedback loops**: modifying the observed DOM inside the callback triggers more records. Guard with a flag/attribute check, or `disconnect()` -> mutate -> `observe()` again.
- `subtree: true` on `document.body` with `attributes: true` on a busy page can generate many records - narrow the root and use `attributeFilter`.
- Do not use it to detect element size/visibility - use `ResizeObserver` / `IntersectionObserver`.
- Call `disconnect()` in component teardown.
- Wait for an element: wrap in a Promise that resolves on first match and disconnects, with a timeout.

## Verify
Check that callback time stays small during heavy DOM updates; unit test by inserting nodes and awaiting a microtask.

## Checked

2026-10-26. MDN MutationObserver, observe() (one of childList, attributes, characterData required, otherwise TypeError) and the microtask guide (Mutation Observer callbacks run from the microtask queue). Removed the unconfirmed shadow-root, garbage-collection and per-frame statements.

Method: documentation only; no commands were run.
