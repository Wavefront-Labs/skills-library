---
id: computing-software.web-development.frontend-development.testing-for-xss
name: testing-for-xss
category: computing-software
field: web-development
product: frontend-development
tags: [stored-xss, reflected-xss, dom-xss-testing, xss-payloads, dom-invader, security-testing]
level: practitioner
status: docs-checked
description: "Finding XSS in your own app: mapping reflection contexts, context-specific probe payloads, stored and blind XSS in admin views, DOM XSS tooling, and regression tests."
sources:
  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting
  - https://portswigger.net/burp/documentation/desktop/tools/dom-invader
  - https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing for XSS

Only test systems you own or are authorised to test.

## 1. Map inputs to outputs
For every input (query params, path segments, form fields, headers like `Referer`, file names, JSON fields, webhook payloads) find where it is rendered: HTML body, attribute, URL attribute, `<script>` block, inline event handler, CSS, or a JS sink (`innerHTML`, `eval`, `location`). Use a unique marker (`zq7x91`) and search the response/DOM for it.

## 2. Probe per context
| Context | Probe | Vulnerable if |
|---|---|---|
| HTML body | `<svg onload=alert(document.domain)>` | tag renders |
| Quoted attribute | `"><svg onload=alert(1)>` / `" autofocus onfocus=alert(1) x="` | quote breaks out |
| URL attribute | `javascript:alert(1)` | link executes |
| JS string | `'-alert(1)-'`, `</script><svg onload=alert(1)>` | string/script breaks |
| Template expression (Angular/Vue client templates on server-rendered HTML) | `{{constructor.constructor('alert(1)')()}}` | expression evaluates |
Use `alert(document.domain)` (or `console.log`) to confirm which origin executes. Test with CSP disabled too: CSP may hide a real injection bug that a CSP change later exposes.

## 3. Stored and blind XSS
Inject into profile names, comments, support tickets, filenames; then view them in **every** place they render: admin panels, emails, PDF exports, CSV opened in tools, logs viewers. For views you cannot see (internal tools), use a payload that calls back to a server you control (blind XSS).

## 4. DOM XSS
Sources: `location.hash/search`, `document.referrer`, `postMessage`, `localStorage`, `window.name`. Burp's DOM Invader, or DevTools breakpoints on DOM sinks such as `innerHTML`. MDN's Trusted Types page lists the injection sinks that enforce trusted types.

## 5. Automate
- Static: search or lint for `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `|safe`, `html_safe`, `raw`.
- Dynamic: an authorised scanner run against staging.
- Regression: unit-test renderers with a payload list and assert the output is inert text.

## Verify
- [ ] Every finding has a test that fails before the fix and passes after.
- [ ] Admin/internal views were included in stored-XSS testing.

## Checked
2026-10-28. Confirmed: OWASP testing guide and PortSwigger cheat sheet cover the probe payloads and `window.name` source; DOM Invader is a Burp tool per the cited page; MDN Trusted Types lists sinks. Removed: report-only claim and named scanners/rule sets not on the fetched pages.
Method: documentation only; no commands were run.
