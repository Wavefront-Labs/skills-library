---
id: computing-software.software-engineering.javascript.js-csp-trusted-types
name: js-csp-trusted-types
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, trusted-types, js-security]
level: advanced
status: docs-checked
description: "Deploy a nonce-based strict CSP, report-only testing and Trusted Types directives to block DOM XSS sinks."
sources: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content Security Policy and Trusted Types

- Strict CSP: MDN recommends nonce- or hash-based fetch directives. A nonce-based one is `script-src 'nonce-{RANDOM}'; object-src 'none'; base-uri 'none';` (a hash-based one swaps in hashes). Nonces are the recommended approach for restricting `<script>` and `<style>`.
- Nonce rules: generate a new unpredictable value for every HTTP response, use the same nonce for all `<script>` tags in that document, insert it with a templating engine (static HTML cannot carry a per-response nonce), and note nonces apply only to `<script>` and `<style>` elements. Hashes keep both policy and content static, which suits static pages.
- `'strict-dynamic'` lets a script that has a nonce or hash load further scripts without nonces; it eases third-party scripts but makes the CSP less secure.
- Avoid `'unsafe-inline'` (browsers ignore it in a directive that has nonce or hash expressions) and `'unsafe-eval'` (still honoured alongside nonces or hashes). `trusted-types-eval` can allow `eval()` only where Trusted Types is supported and enabled. Inline event handlers, `javascript:` URLs and `eval()` still need refactoring, for example event handlers to `addEventListener()`.
- Trusted Types: `require-trusted-types-for 'script'` makes the browser accept only trusted type objects at injection sinks such as `Element.innerHTML` and `eval()`; assigning a raw string throws. `trusted-types` lists acceptable policy names so only named policies can create trusted types. A policy's transform function may not actually sanitize, so keep policies few and reviewed.
- Test first with the `Content-Security-Policy-Report-Only` header: violations are reported but not enforced, and it is honoured alongside an enforced `Content-Security-Policy` header. A report-only policy cannot be delivered in a `<meta>` element.
- Reporting: MDN recommends the Reporting API (`Reporting-Endpoints` header plus the CSP `report-to` directive); `report-uri` is deprecated but may be declared alongside until `report-to` is supported everywhere.
- Fix violations by removing the sink or by sanitising inside one policy.

Self-check: injecting an inline script on a test page is blocked and reported.

## Checked

2026-11-08. Confirmed on MDN Content Security Policy guide: strict CSP, nonce and hash rules, `strict-dynamic`, unsafe keywords, Trusted Types directives, report-only and reporting. Removed browser-support statements for Trusted Types, the specific nonce string in a combined `strict-dynamic` example, and the Google CSP Evaluator tip, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
