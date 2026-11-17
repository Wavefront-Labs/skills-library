---
id: computing-software.software-engineering.javascript.js-dom-safe-insertion
name: js-dom-safe-insertion
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, insertadjacenthtml, js-dom-manipulation]
level: practitioner
status: docs-checked
description: "Insert content with textContent, setHTML and insertAdjacentHTML, treat HTML strings as XSS sinks, and traverse with closest and matches."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML", "https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML", "https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML", "https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent", "https://developer.mozilla.org/en-US/docs/Web/API/Element/closest", "https://developer.mozilla.org/en-US/docs/Web/API/Element/matches"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe HTML insertion and traversal

- Use `textContent` for plain text: it sets a single text node and parses no markup.
- `innerHTML` and `insertAdjacentHTML()` parse their input as HTML and are injection sinks. Neither sanitises: `<script>` and event-handler attributes are not removed. MDN recommends passing `TrustedHTML` and enforcing Trusted Types with the `require-trusted-types-for` CSP directive.
- `Element.setHTML(input, options)` parses and sanitises, always removing XSS-unsafe elements and attributes (`<script>`, `<iframe>`, event handlers and others). MDN marks it Limited availability, so feature-detect it.
- `insertAdjacentHTML(position, input)` does not reparse the element it is called on, so it does not disturb existing children and is much faster than rewriting `innerHTML`.
- Traversal: `el.closest(sel)` returns the nearest ancestor-or-self matching the selector, or `null`; `el.matches(sel)` tests the element.

Self-check: a string like `<img src='x' onerror='alert(1)'>` assigned through `textContent` appears as literal text and does not run.

## Checked

2026-11-03. Confirmed on MDN: Element.insertAdjacentHTML (no sanitisation, no reparse, faster than innerHTML, TrustedHTML advice), Element.innerHTML (injection sink; the `<img ... onerror>` payload appears as the page's own XSS example), Element.setHTML (sanitises, removed element list, Limited availability), Node.textContent, Element.closest, Element.matches. Removed: DOMPurify recommendation, the claim that `innerHTML +=` destroys listeners, and the static/live NodeList and property-vs-attribute bullets (covered in js-dom-selection-and-manipulation).
Method: documentation only; no commands were run.
