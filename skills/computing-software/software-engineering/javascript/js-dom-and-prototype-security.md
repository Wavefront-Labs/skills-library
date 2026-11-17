---
id: computing-software.software-engineering.javascript.js-dom-and-prototype-security
name: js-dom-and-prototype-security
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-xss, dom-xss, prototype-pollution, content-security-policy, trusted-types]
level: advanced
status: draft
description: "Prevent DOM XSS and prototype pollution in JavaScript with safe sinks, CSP and Trusted Types."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DOM XSS and prototype pollution

- Dangerous sinks: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, string `setTimeout`, `location = userValue` (`javascript:` URLs), `href`/`src` from user data. Use `textContent`, `setAttribute` with validated URLs (allow `http:`/`https:` only), or sanitise HTML with DOMPurify. `Element.setHTML()` with the Sanitizer API is emerging; check support.
- Sources: `location.hash/search`, `document.referrer`, `postMessage` (always verify `event.origin`), storage.
- CSP: `Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-...'` blocks inline script injection; avoid `'unsafe-inline'`/`'unsafe-eval'`. Add `require-trusted-types-for 'script'` to enforce Trusted Types where supported.
- Prototype pollution: unsafe recursive merge/`set(path)` with keys `__proto__`, `constructor`, `prototype` mutates `Object.prototype`. Defend: skip those keys, use `Object.create(null)` or `Map`, `Object.hasOwn`, freeze `Object.prototype` in hardened environments, upgrade lodash/others.
- Cookies: `HttpOnly; Secure; SameSite`.
