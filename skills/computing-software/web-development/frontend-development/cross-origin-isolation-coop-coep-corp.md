---
id: computing-software.web-development.frontend-development.cross-origin-isolation-coop-coep-corp
name: cross-origin-isolation-coop-coep-corp
category: computing-software
field: web-development
product: frontend-development
tags: [security-headers, http-security-headers, coop-coep, cross-origin-isolation, cross-origin-opener-policy, cross-origin-embedder-policy, corp, spectre]
level: practitioner
status: docs-checked
description: "Applying COOP, COEP and CORP: isolating your window from cross-origin openers, enabling crossOriginIsolated, and fixing resources and popups that break."
sources:
  - https://web.dev/articles/coop-coep
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy
  - https://github.com/mdn/browser-compat-data/blob/main/http/headers/Cross-Origin-Embedder-Policy.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-origin isolation: COOP, COEP, CORP

**Goal:** protect pages from cross-window attacks (XS-Leaks, tabnabbing) and, when needed, unlock SharedArrayBuffer and precise timers.

## 1. The three headers
| Header | On | Effect |
|---|---|---|
| `Cross-Origin-Opener-Policy: same-origin` | Your documents | Cross-origin windows you open/that open you get no `window.opener` reference; separate browsing context group |
| `Cross-Origin-Embedder-Policy: require-corp` or `credentialless` | Your documents | Every cross-origin subresource must opt in (CORS or CORP), or (credentialless) is loaded without cookies |
| `Cross-Origin-Resource-Policy: same-origin / same-site / cross-origin` | Your resources | Who may embed this resource in no-cors mode |

COOP also accepts `unsafe-none`, `same-origin-allow-popups` and `noopener-allow-popups`. COOP `same-origin` plus COEP `require-corp` (or `credentialless`) makes `self.crossOriginIsolated` true, which gates `SharedArrayBuffer` and unthrottled `performance.now()`.

## 2. COOP side effects
`same-origin` breaks flows that rely on `window.opener` across origins, such as OAuth or payment popups that post back to the opener. MDN names `same-origin-allow-popups` for this case (a cross-origin service for OAuth or payments): the opener page uses it instead of `same-origin`. Alternatively switch the flow to redirects.

## 3. Rolling out COEP
1. Send `Cross-Origin-Embedder-Policy-Report-Only: require-corp` with a reporting endpoint (`Reporting-Endpoints` header; `Report-To` is deprecated); collect what would break.
2. For your own CDN assets add `Cross-Origin-Resource-Policy: cross-origin` (or serve with CORS and `crossorigin` attribute).
3. Third-party images/scripts that don't send CORP: use `credentialless` (requests them without cookies; Chrome 96+, Firefox 119+, not Safari per MDN browser-compat data) or proxy them.
4. COEP applies to resources in iframes and nested frames as well, so embedded frames must be compatible.

## 4. CORP for your APIs/assets
Set `Cross-Origin-Resource-Policy: same-site` (or `same-origin`) on authenticated JSON/images that shouldn't be embeddable by other sites; CORP makes the browser block `no-cors` cross-origin requests for the resource.

## Verify
- [ ] Console: `crossOriginIsolated` is `true` (if you need it) and no COEP blocks.
- [ ] OAuth/payment popups still complete.
- [ ] DevTools > Application > Frames shows the isolation status per frame.

## Checked
Checked 2026-10-26 against MDN (COOP, COEP, CORP pages and browser-compat-data: COEP Chrome 83 / Firefox 79 / Safari 15.2; credentialless Chrome 96 / Firefox 119 / no Safari) and web.dev coop-coep (last updated page text: Report-Only dry run, Reporting-Endpoints replacing Report-To, Application > Frames shows isolation status, CORP values same-origin/same-site/cross-origin). Removed the unconfirmed Spectre-mitigation wording and the unconfirmed claim that third-party iframes need their own COEP header.

Method: documentation only; no commands were run.
