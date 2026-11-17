---
id: computing-software.web-development.frontend-development.dom-xss-sinks
name: dom-xss-sinks
category: computing-software
field: web-development
product: frontend-development
tags: [xss, dom-xss, dangerous-sinks, innerhtml, javascript-urls, security]
level: practitioner
status: docs-checked
description: "Finding and fixing DOM-based XSS: sources like location.hash and postMessage, sinks like innerHTML, eval, document.write and javascript: URLs, and safe replacements."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
  - https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
  - https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API
  - https://github.com/mozilla/eslint-plugin-no-unsanitized
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOM XSS sinks

DOM XSS never touches the server: attacker-controlled **sources** flow into dangerous **sinks** in client JS. Server-side scanners and WAFs miss it.

## 1. Sources
`location.href/search/hash`, `document.referrer`, `window.name`, `postMessage` data, URL params read by routers, `localStorage` values written from other inputs, API responses containing user content.

## 2. Sinks and replacements
| Sink | Safe alternative |
|---|---|
| `el.innerHTML = x`, `outerHTML`, `insertAdjacentHTML` | `el.textContent = x`, `createElement` + `textContent`, or sanitise with DOMPurify |
| `document.write` | DOM APIs |
| `eval`, `new Function`, `setTimeout("string")` | pass functions; `JSON.parse` for data |
| `a.href = x`, `location = x`, `iframe.src = x`, `form.action = x` | validate: `new URL(x, location.origin)` and allow only `http:`/`https:` (block `javascript:`, `data:`) |
| `iframe.srcdoc = x` | sanitise, or use `sandbox` |
| `script.src = x`, `import(x)` | static allowlist |

```js
function safeHref(input) {
  try { const u = new URL(input, location.origin); return ["http:", "https:", "mailto:"].includes(u.protocol) ? u.href : "#"; }
  catch { return "#"; }
}
```

## 3. postMessage
```js
addEventListener("message", e => {
  if (e.origin !== "https://widget.example.com") return;   // check origin first
  if (typeof e.data?.height !== "number") return;          // validate shape
  frame.style.height = `${e.data.height}px`;
});
```

## 4. Framework notes
Frameworks escape text, but escape hatches reach the sinks above: MDN notes React's `dangerouslySetInnerHTML` uses `innerHTML` internally. Validate URLs you bind to `href` (see the URL validation skill). MDN's own XSS example is a template literal assigned to `innerHTML` (`welcome.innerHTML = \`Welcome back, ${user}!\``); string-built HTML is the pattern to look for.

## 5. Find them
- Grep: `innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval\(|new Function`.
- ESLint: `eslint-plugin-no-unsanitized` flags assignments to `innerHTML` and calls such as `insertAdjacentHTML` and `document.write()` unless the input is escaped.
- Enforce with Trusted Types.

## Verify
Test your own pages with benign probes in the hash and query (for example an `<img src=x onerror=...>` string that only logs) and a `?next=javascript:` URL, and confirm nothing executes.

## Checked
Checked 2026-10-26 against the OWASP DOM based XSS Prevention Cheat Sheet (outerHTML, document.write, implicit eval via setTimeout/setInterval/Function), MDN XSS and Element.innerHTML (script elements do not run but onerror payloads do; React dangerouslySetInnerHTML uses innerHTML) and the eslint-plugin-no-unsanitized README. Removed unconfirmed items: the jQuery and Range.createContextualFragment rows, the claim that React renders javascript: hrefs, the Semgrep ruleset name and Burp DOM Invader. The safeHref snippet was not run.

Method: documentation only; no commands were run.
