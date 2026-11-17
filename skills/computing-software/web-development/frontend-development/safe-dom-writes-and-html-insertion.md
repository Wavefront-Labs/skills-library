---
id: computing-software.web-development.frontend-development.safe-dom-writes-and-html-insertion
name: safe-dom-writes-and-html-insertion
category: computing-software
field: web-development
product: frontend-development
tags: [replacechildren, insertadjacenthtml, sethtml, sanitizer-api, innerhtml, dom-manipulation]
level: practitioner
status: docs-checked
description: "Choosing DOM write APIs: textContent, append/replaceChildren, insertAdjacentHTML, innerHTML pitfalls, setHTML with the Sanitizer API and setHTMLUnsafe for shadow roots."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTMLUnsafe
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/replaceChildren
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/innerText
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe DOM writes and HTML insertion

## 1. Decision table
| Content | API | Notes |
|---|---|---|
| Plain text | `el.textContent = s` | never parses HTML; fastest |
| New nodes | `el.append(node, "text")`, `before/after/replaceWith` | strings become text nodes |
| Replace all children | `el.replaceChildren(...nodes)` | `replaceChildren()` with no args clears |
| Trusted HTML at a position | `el.insertAdjacentHTML("beforeend", html)` | does not re-parse existing children |
| Untrusted HTML | `el.setHTML(html)` (Sanitizer API) or DOMPurify + `innerHTML` | sanitises |
| HTML with declarative shadow DOM | `el.setHTMLUnsafe(html)` / `Document.parseHTMLUnsafe()` | unsanitised; unlike `innerHTML` it parses declarative shadow roots, so use only on trusted input |

## 2. innerHTML pitfalls
- `el.innerHTML += row` re-serialises and re-parses the element's existing content, whereas MDN says `insertAdjacentHTML()` does not reparse the element it is used on and so does not corrupt existing elements. Use `insertAdjacentHTML("beforeend", row)` or `append`.
- Any untrusted value is XSS: MDN notes `innerHTML` stops `<script>` elements from running but an `<img src=x onerror=...>` payload still executes.
- `innerText` is aware of rendered appearance (CSS) while `textContent` is not; prefer `textContent` for plain text.

## 3. Building lists efficiently
```js
const tpl = document.querySelector("#row");
const frag = document.createDocumentFragment();
for (const item of items) {
  const row = tpl.content.cloneNode(true);
  row.querySelector(".name").textContent = item.name;   // text, not HTML
  frag.append(row);
}
list.replaceChildren(frag);   // one insertion, one layout
```

## 4. Sanitizer API
```js
if ("setHTML" in Element.prototype) el.setHTML(userHtml);              // default safe config strips script/handlers
else el.innerHTML = DOMPurify.sanitize(userHtml);
el.setHTML(userHtml, { sanitizer: { elements: ["p", "b", "i", "a"], attributes: ["href"] } });   // a SanitizerConfig
```
MDN browser-compat data: `setHTML` Chrome 146 and Firefox 148, not Safari; feature-detect and keep DOMPurify as fallback. Under Trusted Types enforcement `innerHTML` and `insertAdjacentHTML` need a `TrustedHTML` value; MDN says `setHTML()` always sanitises, so it is not checked by Trusted Types. The `sanitizer` option takes a `Sanitizer`, a `SanitizerConfig` or the string `"default"`, and XSS-unsafe elements and attributes are removed even if your config allows them.

## Gotchas
- Build table rows with `<template>` and DOM methods instead of string-concatenating `<tr>` into a `<div>`; HTML parsing drops table elements outside a table context.

## Verify
- [ ] Grep for `innerHTML\s*\+=` and `innerHTML =` with interpolated variables; each is justified or replaced.
- [ ] Trusted Types report-only mode shows no violations.

## Checked
Checked 2026-10-26 against MDN Element.setHTML (options.sanitizer accepts Sanitizer, SanitizerConfig or "default"; always removes XSS-unsafe content; not validated by Trusted Types), setHTMLUnsafe (parses declarative shadow roots), insertAdjacentHTML (does not reparse existing content, no sanitisation), replaceChildren (empties a node), innerHTML (script elements do not run, onerror payloads do), innerText vs textContent, and MDN browser-compat data (setHTML Chrome 146, Firefox 148; setHTMLUnsafe Chrome 124, Firefox 123, Safari 26). Removed unconfirmed items: the memory-leak remark about remove() and listeners and the unverified insertAdjacentHTML table-context claim. The snippets were not run.

Method: documentation only; no commands were run.
