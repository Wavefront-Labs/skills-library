---
id: computing-software.qa-testing-engineering.test-automation.xss-and-csrf-testing
name: xss-and-csrf-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [xss-testing, csrf-testing, security-testing, content-security-policy]
level: advanced
status: docs-checked
description: "Test for XSS and CSRF using the OWASP cheat sheets as the expected-behaviour baseline: output encoding by context, unsafe sinks, CSP, tokens and SameSite."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XSS and CSRF testing

**Goal:** show that user input is never executed as script in another user's browser, and that state-changing requests cannot be forged cross-site. Authorised targets only. The OWASP cheat sheets describe the defences; each test below checks that a defence is in place.

## XSS
1. **Find sinks:** every place input is echoed: search results, profile fields, error messages, file names, rich text, and URL fragments read by JavaScript.
2. **Probe with a harmless marker** first and check how it comes back in the HTML source, because browsers parse HTML, JavaScript, URLs and CSS differently and the right encoding depends on the context (HTML body, quoted attribute, JavaScript, CSS).
3. **Expected behaviour per context** (cheat sheet):
   - HTML body: values are HTML entity encoded; a payload such as `<script>alert`1`</script>` must display as text.
   - Attributes: ordinary text attributes (`title`, `value`) are encoded and quoted. Event-handler attributes and `srcdoc` can interpret their values as code or HTML, so user data must not reach them.
   - JavaScript: untrusted code, identifiers or expressions are never inserted; passing an encoded value to `eval()` or another code-interpreting sink is still unsafe.
   - CSS: variables only in a CSS property value; other CSS contexts are unsafe.
   - JSON responses: `Content-Type` is `application/json`, not `text/html`.
4. **Stored XSS:** submit as one user and view as another (including admin consoles, exports and emails that render the value).
5. **Framework escape hatches** the cheat sheet names as risky: React `dangerouslySetInnerHTML` without sanitising, Angular `bypassSecurityTrustAs*`, Lit `unsafeHTML`, and Polymer `inner-h-t-m-l`. Unvalidated URL values also need application checks (React 19 blocks `javascript:` URLs in `src` and `href` but this does not replace validation).
6. **DOM XSS:** look for unsafe sinks such as `innerHTML`, `document.write` with `document.location.hash`, and `eval()`, `setInterval()`, `setTimeout()` called with untrusted strings. Safe alternatives named by the cheat sheet: `textContent`, `value`, and `DOMPurify.sanitize()` before `innerHTML`.
7. **CSP:** a Content-Security-Policy is an additional layer, not the primary defence; review the policy but do not treat its presence as proof the application is free of XSS.

## CSRF
- List state-changing requests. The cheat sheet says not to use GET for them; any GET that changes state is a defect.
- Token check: remove or alter the anti-CSRF token and the server must reject the request; so must a token from another session. Tokens should be unique per session, secret and unpredictable, must not be sent in a cookie for the synchronizer pattern, and must not leak into URLs or logs.
- SameSite: `Strict` withholds cookies on all cross-site requests, `Lax` sends them on top-level navigations using safe methods, so `Lax` does not stop a state-changing GET. Browser defaults vary (Chromium treats cookies without the attribute as Lax; Firefox and Safari do not) so check the cookie sets `SameSite` explicitly. SameSite does not protect against client-side CSRF.
- Simple requests: form content types (`application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`) are not preflighted. A JSON API that also accepts `text/plain` is vulnerable; test that it rejects those content types.
- Custom request headers on API calls rely on CORS preflight; test that the API requires the header.
- Modern browsers: Fetch Metadata (`Sec-Fetch-Site: cross-site`) can be used to reject cross-site non-safe methods.
- XSS can defeat all CSRF mitigations, so test XSS first.

## Verify
Each input sink has a recorded result per context, and token-removal and cross-origin attempts are rejected for every state-changing endpoint.

## Checked
2026-11-09: checked against the OWASP XSS Prevention and CSRF Prevention cheat sheets (the XSS page read through output encoding and DOM sections, the CSRF page through token, SameSite, simple-request and Fetch Metadata sections; later sections on framework-specific recipes were not read). Removed because the cheat sheets do not state them: the WSTG source (its deep link redirects to a landing page), the specific attack payload strings for attributes and JavaScript strings, `qa"'<x>${7*7}` marker, Burp DOM Invader, Google CSP Evaluator, the claim that `unsafe-inline` or `*` always leaves XSS exploitable, and the 403 status expectation. Tag `owasp-wstg` trimmed.

Method: documentation only; no commands were run.
