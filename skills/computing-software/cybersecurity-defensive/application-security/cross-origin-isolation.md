---
id: computing-software.cybersecurity-defensive.application-security.cross-origin-isolation
name: cross-origin-isolation
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [cross-origin-isolation, coop, coep, corp, spectre, xs-leaks, security-headers]
level: advanced
status: docs-checked
description: "Deploy COOP, COEP and CORP headers for cross-origin isolation: defend against XS-Leaks and Spectre, enable SharedArrayBuffer, and handle popups and third-party embeds."
sources: ["https://web.dev/articles/coop-coep", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy", "https://xsleaks.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-origin isolation (COOP, COEP, CORP)

## The three headers
- **Cross-Origin-Opener-Policy (COOP)**: separates your top-level window from cross-origin windows it opens or
  is opened by. `same-origin` breaks the `window.opener` reference with cross-origin pages, blocking many
  XS-Leak and tabnabbing attacks. `same-origin-allow-popups` keeps references to popups you open (needed for
  some OAuth/payment popup flows). `noopener-allow-popups` is a newer value.
- **Cross-Origin-Embedder-Policy (COEP)**: `require-corp` makes the document load only cross-origin resources
  that explicitly opt in (via CORS or CORP). `credentialless` loads no-cors cross-origin resources without
  cookies instead of requiring opt-in (easier with third-party images).
- **Cross-Origin-Resource-Policy (CORP)**: set on resources: `same-origin`, `same-site` or `cross-origin`.
  Protects your resources from being loaded by other sites into their process (Spectre-style reads).

## Why
- With COOP `same-origin` + COEP `require-corp` (or `credentialless`), the page is **cross-origin isolated**
  (`self.crossOriginIsolated === true`): enables `SharedArrayBuffer` and high-resolution timers safely.
- Even without full isolation, COOP alone is a cheap defence for sensitive apps (banking, admin), and CORP
  `same-origin` on authenticated API responses and private images limits cross-site embedding.

## Rollout
1. Add the report-only variant of COEP first (`Cross-Origin-Embedder-Policy-Report-Only`) to see what would break, with a reporting endpoint configured.
2. Fix breakage: third-party resources need CORS (`crossorigin` attribute plus ACAO header) or CORP
   `cross-origin`; iframes need their own COEP-compatible headers; OAuth popups may need
   `same-origin-allow-popups`.
3. Enforce COOP on sensitive pages, then COEP where isolation is required.
4. Set `Cross-Origin-Resource-Policy: same-origin` on private API and user-content responses.

## Gotchas
- COEP `require-corp` breaks embeds that do not send CORP/CORS (ads, some analytics, YouTube embeds without
  `credentialless`).
- COOP breaks flows depending on `window.opener` across origins (some SSO, payment popups).
- These headers are per response; HTML documents need COOP/COEP, subresources need CORP.

## Verify
DevTools console `self.crossOriginIsolated` returns true where intended; Network panel shows no COEP blocked
resources; a cross-origin page opening your site gets `null` for `window.opener`.

## Checked
2026-10-28. Confirmed against official pages: COOP values including noopener-allow-popups, COEP require-corp and credentialless, crossOriginIsolated (MDN COOP and COEP pages, web.dev COOP/COEP guide), COEP report-only (web.dev).
Removed or rewritten: the COOP report-only header example and the report-to names.
Method: documentation only; no commands were run.
