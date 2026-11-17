---
id: computing-software.web-development.frontend-development.referrer-policy-nosniff-and-permissions-policy
name: referrer-policy-nosniff-and-permissions-policy
category: computing-software
field: web-development
product: frontend-development
tags: [security-headers, http-security-headers, referrer-policy, permissions-policy, x-content-type-options, nosniff, helmet]
level: practitioner
status: docs-checked
description: "Setting X-Content-Type-Options nosniff, Referrer-Policy and Permissions-Policy correctly, and the legacy headers you can drop."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
  - https://github.com/helmetjs/helmet#readme
  - https://nginx.org/en/docs/http/ngx_http_headers_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Referrer-Policy, nosniff and Permissions-Policy

**Goal:** a baseline header set that closes MIME-sniffing, URL leakage and unwanted powerful-feature access.

## 1. Baseline
```
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
Cross-Origin-Opener-Policy: same-origin
```

## 2. X-Content-Type-Options: nosniff
Stops browsers guessing a type: a script/style served with the wrong `Content-Type` is refused. Consequence: your server must send correct types (`text/javascript`, `text/css`, `application/json`). Blocks attacks where an uploaded "image" is executed as script.

## 3. Referrer-Policy
`strict-origin-when-cross-origin` (the default when no policy is set, per MDN): full URL same-origin, only the origin cross-origin, nothing on HTTPS to HTTP downgrade. Use `no-referrer` or `same-origin` on pages whose URLs carry secrets (password reset tokens, invite links) - and better, don't put secrets in URLs. Per-element override: `<a rel="noreferrer">` or the `referrerpolicy` attribute; a whole-document override is `<meta name="referrer" content="no-referrer">`. A header may list a fallback value first, e.g. `no-referrer, strict-origin-when-cross-origin`.

## 4. Permissions-Policy
Allows or denies features for your document and its iframes: `geolocation=(self "https://maps.example.com")`. Iframes also need an `allow` attribute (for example `allow="geolocation"`). Allowlist values: `*` (all), `()` (none), `self`, and quoted origins; `*` and `()` can only be used alone. MDN browser-compat data lists the `Permissions-Policy` header as supported in Chromium only (Chrome 85+), so treat it as an extra layer, not a baseline for Firefox or Safari.

## 5. Drop / don't bother
- `X-XSS-Protection`: Rails 7.0+ sends `0` by default (Rails 8.2 drops it); do not rely on the old browser XSS filter.
- `X-Powered-By`: Helmet removes it by default; hygiene only, not a real control.

## 6. Applying
Express: `helmet()` sets a default header set (it sets `X-Content-Type-Options: nosniff` and a `Referrer-Policy` of `no-referrer`, so override it if you want `strict-origin-when-cross-origin`); nginx: `add_header … always;` (`add_header` directives are inherited only if the current level defines none); Django: `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_REFERRER_POLICY`.

## Verify
- [ ] securityheaders.com / Mozilla Observatory grade A without CSP exceptions you didn't intend.
- [ ] Static assets have correct `Content-Type` (no nosniff blocks in console).
- [ ] In Chromium, DevTools > Application > Frames shows the effective permissions policy for the feature you disabled.

## Checked
Checked 2026-10-26 against MDN (Referrer-Policy: default strict-origin-when-cross-origin, fallback list, rel=noreferrer, meta name referrer; Permissions-Policy allowlist syntax and Chromium-only support from browser-compat data; X-Content-Type-Options), the Helmet README (nosniff, Referrer-Policy default no-referrer, X-Powered-By removed), the nginx ngx_http_headers_module source (add_header inheritance and always) and the Rails configuration guide (X-XSS-Protection 0 from 7.0, removed in 8.2 defaults). Removed unconfirmed items: usb and interest-cohort tokens, Expect-CT and Public-Key-Pins remarks, the Next.js headers note and the document.featurePolicy check.

Method: documentation only; no commands were run.
