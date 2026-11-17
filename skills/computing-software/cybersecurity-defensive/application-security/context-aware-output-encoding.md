---
id: computing-software.cybersecurity-defensive.application-security.context-aware-output-encoding
name: context-aware-output-encoding
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, output-encoding, xss, contextual-escaping, auto-escaping, html-sanitization, dom-xss]
level: practitioner
status: docs-checked
description: "Prevent XSS with context-aware output encoding: framework templating, per-context encoders for HTML, attribute, JavaScript, URL and CSS, safe sinks, and HTML sanitisation."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context-aware output encoding

**Goal:** untrusted data is encoded for the exact context it lands in, so it renders as text, never code.
Browsers parse HTML, JS, URLs and CSS differently; the wrong encoder can leave a weakness or break the page.

## Contexts and encoders (OWASP XSS Prevention Cheat Sheet)
| Context | Control |
|---|---|
| HTML body | HTML encoding; in JavaScript assign text to `textContent` (does not HTML-encode, pass the original text) |
| Ordinary text attribute | Quote the value and use HTML attribute encoding from a framework or library; keep attribute names fixed; URL, CSS, HTML and JavaScript values need extra controls |
| JavaScript string in inline script | Library encoder documented for both the JS string and enclosing HTML script; insert only inside a quoted string; never untrusted code or expressions |
| URL parameter value | Percent-encode the value only (`encodeURIComponent()` in JS), not the whole URL |
| Untrusted URL in `href`/`src` | Canonicalise, validate, allow-list http and HTTPS only, then attribute-encode |
| CSS | Only in a CSS property value, strict validation and CSS hex encoding; JS: fixed property from an allowlist |
| JSON responses | Content-Type `application/json`, not `text/html` |

## Frameworks
Frameworks with templating and auto-escaping reduce XSS, but gaps remain: React `dangerouslySetInnerHTML`
without sanitising, and unvalidated URL values (React 19 blocks `javascript:` in `src`/`href` but that does
not replace your URL validation).

## Dangerous contexts
Do not place variable data in dangerous contexts (directly in `<style>`, as an attribute name, in CSS URL
handling, as an entire event-handler value): encoding does not fully prevent XSS there. Prefer trusted
functions registered with `addEventListener()`.

## Safe sinks and rich HTML
Prefer `textContent` or `value`; `setAttribute(safeName, value)` with a safe name; avoid `innerHTML`. For
user-authored HTML, OWASP recommends DOMPurify: `elem.innerHTML = DOMPurify.sanitize(dirty)`. Do not modify
content after sanitising, check that downstream libraries do not mutate it, and patch the sanitiser
regularly.

## Gotchas
- CSP alone and HTTP interceptors are listed by OWASP as ineffective sole defences; CSP and cookie
  attributes only limit impact.

## Verify
- [ ] Every variable goes through validation and then escaping or sanitising for its context.
- [ ] No variables in dangerous contexts.

## Checked
2026-11-01. Confirmed against the OWASP XSS Prevention Cheat Sheet. Removed: per-engine escape-hatch lists
(Jinja, Django, Thymeleaf, Razor, Vue, Angular), template syntax examples, the Python/.NET sanitiser
library list, Markdown-renderer and double-context advice, and test payloads.
Method: documentation only; no commands were run.
