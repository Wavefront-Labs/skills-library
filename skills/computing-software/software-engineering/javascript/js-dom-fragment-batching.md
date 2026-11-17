---
id: computing-software.software-engineering.javascript.js-dom-fragment-batching
name: js-dom-fragment-batching
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, documentfragment, js-dom-manipulation]
level: practitioner
status: docs-checked
description: "Insert many DOM nodes at once with DocumentFragment, replaceChildren and template cloning, and move nodes instead of copying."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment", "https://developer.mozilla.org/en-US/docs/Web/API/Element/replaceChildren", "https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild", "https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch DOM updates

- Build many nodes in a `DocumentFragment`, then insert it once: `appendChild()` of a fragment returns the emptied fragment.
- `parent.replaceChildren(...nodes)` swaps the whole child set in one call; `parent.replaceChildren()` with no arguments empties the node.
- `appendChild()` moves an existing node rather than copying it; use `cloneNode()` first when you need a copy. `Element.append()` takes several arguments and strings, so prefer it for elements.
- `<template>`: clone `tpl.content` with `cloneNode(true)` for repeated markup.
- `getBoundingClientRect()` returns the element's size and viewport-relative position. Read all measurements together, then write, rather than interleaving reads and writes.
- Toggle classes (`classList.toggle`) instead of writing many inline styles.

Self-check: after the batch, the list has the expected child count and the fragment is empty.

## Checked

2026-11-03. Confirmed on MDN: DocumentFragment, Element.replaceChildren (including the no-argument empty form and spread usage), Node.appendChild (moves nodes, returns the emptied fragment, points to Element.append), Element.classList (toggle), Element.getBoundingClientRect (DOMRect, viewport-relative). Removed: claims that interleaved reads and writes force repeated reflow (offsetHeight), CSS `contain` / `content-visibility`, the "single Layout event" Performance-panel check, and `before/after/remove` wording, none of which are on a page read.
Method: documentation only; no commands were run.
