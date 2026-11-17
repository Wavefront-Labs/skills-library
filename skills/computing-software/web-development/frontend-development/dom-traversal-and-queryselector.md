---
id: computing-software.web-development.frontend-development.dom-traversal-and-queryselector
name: dom-traversal-and-queryselector
category: computing-software
field: web-development
product: frontend-development
tags: [dom-traversal, queryselector, closest, matches, dom, javascript]
level: intro
status: docs-checked
description: "Finding and walking DOM nodes: querySelector/All scoping, :scope, closest() for delegation, matches(), element vs node traversal properties, live vs static lists and TreeWalker."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
  - https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape_static
  - https://developer.mozilla.org/en-US/docs/Web/API/Node/getRootNode
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/createTreeWalker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOM traversal with querySelector, closest and matches

## 1. Querying
```js
const form = document.querySelector("#signup");          // first match or null
const inputs = form.querySelectorAll("input[required]"); // static NodeList, scoped to form
const direct = list.querySelectorAll(":scope > li");     // only direct children of list
```
- Scope to the nearest container instead of `document` to avoid collisions between widgets.
- `querySelectorAll` returns a **static** NodeList (has `forEach`, not `map`): use `[...nodes].map()`.
- `getElementsByClassName` and `children` return **live** HTMLCollections that change as the DOM changes; copy first if you remove nodes.
- Ids starting with a digit or containing `:` need escaping: `document.querySelector("#" + CSS.escape(id))`, or use `getElementById`.

## 2. Walking up: closest and matches
```js
document.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-action]");  // includes the element itself
  if (!btn || !table.contains(btn)) return;              // ignore clicks outside the widget
  handlers[btn.dataset.action]?.(btn);
});
if (el.matches(":focus-visible, [aria-expanded=true]")) { /* ... */ }
```
`e.target` may be an inner `<svg>`/`<span>`; `closest()` normalises that, which makes event delegation robust.

## 3. Element vs node properties
| Use | Avoid (includes text/comment nodes) |
|---|---|
| `parentElement`, `children`, `firstElementChild`, `nextElementSibling` | `parentNode`, `childNodes`, `firstChild`, `nextSibling` |

Whitespace between tags is a text node, so `firstChild` is often `"\n  "`.

## 4. Shadow DOM boundaries
`querySelector` does not search inside shadow roots. Inside a component use `this.shadowRoot.querySelector`; `el.getRootNode()` returns the shadow root (optionally with `composed: true` the document); for events, `e.composedPath()`.

## 5. Bulk walks
`document.createTreeWalker(root, NodeFilter.SHOW_TEXT)` iterates text nodes without recursion.

## Verify
- [ ] Delegated handlers work when clicking icons inside buttons; no loops over live collections that mutate; selectors with user-provided ids go through `CSS.escape`.

## Checked

2026-10-26. MDN querySelectorAll (static NodeList), :scope, Element.closest (matches the element itself, null if none), CSS.escape, Node.getRootNode and createTreeWalker. Removed the unconfirmed speed claim and the claim about closest crossing shadow roots.

Method: documentation only; no commands were run.
