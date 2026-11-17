---
id: computing-software.software-engineering.javascript.js-dom-selection-and-manipulation
name: js-dom-selection-and-manipulation
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-dom, queryselector, createelement, textcontent-vs-innerhtml, classlist]
level: practitioner
status: docs-checked
description: "Select and update DOM nodes with querySelector, live vs static collections, classList, dataset, textContent and fragments."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll", "https://developer.mozilla.org/en-US/docs/Web/API/NodeList", "https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementsByClassName", "https://developer.mozilla.org/en-US/docs/Web/API/Element/classList", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset", "https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent", "https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOM selection and manipulation

- `document.querySelectorAll()` returns a static (non-live) NodeList; `getElementsByClassName()` returns a live HTMLCollection that updates as the DOM changes, so take care when iterating. `document.querySelector()` returns the first match.
- `el.closest(sel)` walks from the element up through its ancestors and returns the first match or `null`; `el.matches(sel)` tests the element itself.
- Create with `document.createElement`, clone `template.content` with `cloneNode(true)`, and insert with `append()` or `replaceChildren()`. Batch inserts with a `DocumentFragment`.
- Text: `textContent` replaces all children with a single text node and does not parse markup. `innerHTML` parses its input as HTML and is an XSS injection sink; never feed it untrusted strings.
- Classes: `el.classList` is a live DOMTokenList with `add()`, `remove()`, `replace()`, `toggle()` and `contains()`.
- Data attributes: `el.dataset.fooBar` reads and writes `data-foo-bar` (dashes removed, next letter capitalised).

## Checked

2026-11-03. Confirmed on MDN: Document.querySelectorAll (static NodeList), NodeList (live vs static), getElementsByClassName (live), Element.closest, Element.matches, Element.classList (add/remove/replace/toggle/contains), HTMLElement.dataset (camel-case mapping), Node.textContent, Element.innerHTML (injection sink warning). Removed: `toggleAttribute`, `before()/after()/remove()`, `input.value` vs attribute, `offsetHeight` reflow note, `DOMContentLoaded` and script placement advice (no page read), and the ECMAScript and MDN JavaScript root sources, which do not cover DOM APIs.
Method: documentation only; no commands were run.
