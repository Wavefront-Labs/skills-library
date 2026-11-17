---
id: computing-software.web-development.frontend-development.clickjacking-and-frame-ancestors
name: clickjacking-and-frame-ancestors
category: computing-software
field: web-development
product: frontend-development
tags: [content-security-policy, csp, frame-ancestors, clickjacking, x-frame-options, framing-protection, iframe-embedding]
level: practitioner
status: docs-checked
description: "Preventing clickjacking with CSP frame-ancestors (and X-Frame-Options fallback), allowing specific partner embeds, and testing framing."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
  - https://docs.djangoproject.com/en/stable/ref/clickjacking/
  - https://github.com/helmetjs/helmet#readme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clickjacking and frame-ancestors

**Goal:** other sites can't load your pages in an invisible iframe and trick users into clicking (delete account, approve payment, change settings).

## 1. Default: deny framing
```
Content-Security-Policy: frame-ancestors 'none'
X-Frame-Options: DENY
```
`frame-ancestors` is the modern control; per the CSP spec, `X-Frame-Options` must be ignored when an enforced `frame-ancestors` is present, and it covers older browsers. Both must be HTTP headers: `frame-ancestors` is not supported in a `<meta>` CSP, and `X-Frame-Options` in a `<meta>` has no effect. `frame-ancestors` does not fall back to `default-src`, so `default-src 'none'` alone still allows framing.

## 2. Allow your own or partner framing
```
Content-Security-Policy: frame-ancestors 'self' https://partner.example.com https://*.example.org
X-Frame-Options: SAMEORIGIN        (the ALLOW-FROM value is deprecated; send SAMEORIGIN or omit the header when partners need to frame the page)
```
`frame-ancestors` checks **every** ancestor in the chain, not just the parent.

## 3. Where to set it
On every HTML response, including error pages and login/OAuth consent pages (the high-value targets). Express: `helmet()` sends `X-Frame-Options: SAMEORIGIN` by default and you add the CSP directive; Django: `XFrameOptionsMiddleware` (setting `X_FRAME_OPTIONS`, default `'DENY'`) plus CSP; Rails: default header `X-Frame-Options: SAMEORIGIN`; other frameworks: add both headers in the server or CDN configuration. Embeddable widgets get a separate route with a looser policy.

## 4. Don't rely on frame-busting JS
Frame-busting scripts (`if (top !== self) top.location = self.location`) can be defeated by framing the page in an `<iframe sandbox>`, so they are not a control. Use headers.

## 5. Related
- `SameSite=Lax`/`Strict` cookies are withheld from cross-site iframe requests, which helps, but SameSite does not block framing and a same-site sibling subdomain can still frame the page. Defence in depth, not a substitute for `frame-ancestors`.
- For pages that **must** be framed cross-site (embeds), require an explicit confirmation step for sensitive actions.

## Verify
- [ ] A test page on another origin with `<iframe src="https://app.example.com/settings">` shows a blocked frame; console mentions frame-ancestors.
- [ ] `curl -sI https://app.example.com/login | grep -i -e frame -e content-security` shows the headers on every route, including 404/500.

## Checked
Checked 2026-10-26 against the current MDN pages for frame-ancestors and X-Frame-Options, the OWASP Clickjacking Defense Cheat Sheet, the Django clickjacking and settings reference (default `X_FRAME_OPTIONS` is `'DENY'`), the Rails configuration guide (default header `X-Frame-Options: SAMEORIGIN`) and the Helmet README (`X-Frame-Options: SAMEORIGIN` default). Confirmed: frame-ancestors unsupported in meta, no default-src fallback, every ancestor checked, ALLOW-FROM deprecated, precedence of frame-ancestors over X-Frame-Options, sandboxed iframe defeats frame-busting, SameSite limits. Removed the unconfirmed Next.js remark.

Method: documentation only; no commands were run.
