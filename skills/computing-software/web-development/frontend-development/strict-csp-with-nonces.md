---
id: computing-software.web-development.frontend-development.strict-csp-with-nonces
name: strict-csp-with-nonces
category: computing-software
field: web-development
product: frontend-development
tags: [content-security-policy, csp, csp-nonce, strict-dynamic, strict-csp, xss-mitigation, script-src, object-src]
level: practitioner
status: docs-checked
description: "Deploying a nonce-based strict Content Security Policy with strict-dynamic: per-response nonces, framework wiring, inline handler removal and fallbacks."
sources:
  - https://web.dev/articles/strict-csp
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
  - https://nextjs.org/docs/app/guides/content-security-policy
  - https://guides.rubyonrails.org/security.html#content-security-policy
  - https://django-csp.readthedocs.io/
  - https://github.com/helmetjs/helmet#readme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strict CSP with nonces

**Goal:** a CSP that actually stops injected scripts (allowlist CSPs like `script-src 'self' cdn.example.com` are usually bypassable via JSONP/old libraries on allowed hosts).

## 1. The policy
```
Content-Security-Policy:
  script-src 'nonce-{RANDOM}' 'strict-dynamic' https: 'unsafe-inline';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'self';
  report-to csp-endpoint
```
(`report-to` names an endpoint declared in the `Reporting-Endpoints` header.)
- `'nonce-…'`: only `<script nonce="…">` with the matching value runs.
- `'strict-dynamic'`: scripts loaded **by** a trusted script are trusted too (bundler chunks, tag managers), and host allowlists/`'self'` are ignored by supporting browsers.
- `https: 'unsafe-inline'` are fallbacks: web.dev says all browsers that support `strict-dynamic` ignore `https:`, and recent browsers ignore `'unsafe-inline'` when a nonce or hash is present (MDN says the same); they keep older browsers working.
- `object-src 'none'` and `base-uri 'none'` close plugin and `<base>` hijacks.

## 2. Nonce rules
- Fresh cryptographically random value **per response** (web.dev: ideally 128+ bits, base64 encoded), for example `crypto.randomBytes(16).toString('base64')` in Node. A static nonce is no protection.
- Pages with nonces can't be served from a shared cache unchanged (the nonce must differ per response) - render per request, or use hash-based CSP for static pages (see the hash-based-csp-for-static-sites skill).
- Add `nonce` to every `<script>` you emit, including inline JSON bootstraps and analytics snippets.

## 3. Framework wiring
- **Express**: middleware sets `res.locals.cspNonce`; with Helmet pass a function in `contentSecurityPolicy.directives.scriptSrc`, e.g. `(req, res) => "'nonce-" + res.locals.cspNonce + "'"` (the Helmet README example), and print the nonce into each `<script>`.
- **Next.js (App Router)**: generate the nonce in the Proxy (formerly middleware) file, set the `Content-Security-Policy` header and an `x-nonce` request header, and read it with `(await headers()).get('x-nonce')` for your own scripts. Next.js docs: nonces require dynamic rendering.
- **Django**: `django-csp` (current versions configure the policy in a `CONTENT_SECURITY_POLICY` setting with `DIRECTIVES`; the middleware exposes a lazily generated `request.csp_nonce` for templates, e.g. `<script nonce="{{request.csp_nonce}}">`; check its docs for how to add the nonce source to a directive); **Rails**: set `content_security_policy_nonce_generator` and use `javascript_tag nonce: true` (the Security Guide also shows `javascript_include_tag "script", nonce: true`).

## 4. Refactor what CSP blocks
- Inline event handlers (`onclick="…"`) and `javascript:` URLs are blocked by nonces - move to `addEventListener`.
- `eval`/`new Function`/string `setTimeout` need `'unsafe-eval'` - remove them (some template compilers need a runtime-only build).
- Inline `style=` attributes fall under `style-src`; `'unsafe-inline'` weakens it, so tighten later.

## Verify
- [ ] CSP Evaluator rates the policy without high-severity findings.
- [ ] Injecting `<script>alert(1)</script>` and `<img src=x onerror=alert(1)>` in a test field does nothing and produces a violation report.
- [ ] Nonce differs on every reload (view source twice).

## Checked
Checked 2026-10-26 against web.dev strict-csp (updated 2024-09-13: policy template, 128+ bit base64 nonce regenerated per response, fallbacks ignored by supporting browsers), MDN CSP guide (nonce and hash make unsafe-inline ignored; strict-dynamic), the Helmet README (res.locals.cspNonce with a scriptSrc function), the Next.js CSP guide (Proxy sets x-nonce; dynamic rendering required; headers().get('x-nonce')), the django-csp docs (CONTENT_SECURITY_POLICY with DIRECTIVES, request.csp_nonce) and the Rails Security Guide (content_security_policy_nonce_generator, javascript_tag nonce: true). Replaced the outdated django-csp CSP_INCLUDE_NONCE_IN setting and the Next.js 'middleware' wording. CSP Evaluator and the injection tests were not run.

Method: documentation only; no commands were run.
