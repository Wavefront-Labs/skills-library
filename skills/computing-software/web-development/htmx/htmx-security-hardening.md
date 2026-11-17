---
id: computing-software.web-development.htmx.htmx-security-hardening
name: htmx-security-hardening
category: computing-software
field: web-development
product: htmx
tags: [htmx, security, xss, hx-disable, csp, csrf, selfrequestsonly, alloweval]
level: advanced
status: docs-checked
description: "Harden an htmx app: escape user content, hx-disable around untrusted HTML, selfRequestsOnly, allowEval/allowScriptTags, validateUrl, CSP and CSRF headers."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-disable.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-history.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop injected HTML from abusing htmx's expressiveness. If an attacker can inject markup with `hx-*` attributes they can make requests, so layer defences.

1. Escape all user content (Rule 1). Use your template engine's auto-escaping. If you inject raw HTML (`raw()` helpers), scrub third-party content, removing attributes beginning `hx-` and `data-hx` and inline `<script>`; prefer allow-listing tags/attributes over deny-listing.
2. `hx-disable`: on a wrapper, htmx ignores all htmx attributes on it and all descendants. The value is ignored; content below cannot undo it (any `hx-disable` found up the parent chain wins).
```html
<div hx-disable><%= raw(user_content) %></div>
```
The selector is configurable via `htmx.config.disableSelector` (default `[hx-disable], [data-hx-disable]`).
3. History cache: put `hx-history="false"` on pages with sensitive data, or set `htmx.config.historyCacheSize = 0`.
4. Config switches:
   - `htmx.config.selfRequestsOnly` (default `true`): only same-domain requests.
   - `htmx.config.allowScriptTags` (default `true`): set `false` so `<script>` in loaded content is not processed.
   - `htmx.config.allowEval` (default `true`): set `false` to disable event filters, `hx-on:` attributes, `hx-vals`/`hx-headers` with `js:` (reimplement via custom JS and htmx events).
5. Allow specific other hosts: listen for `htmx:validateUrl`, inspect `evt.detail.url.hostname` and `evt.detail.sameHost`, and call `evt.preventDefault()` to block.
```javascript
document.body.addEventListener('htmx:validateUrl', e => {
  if (!e.detail.sameHost && e.detail.url.hostname !== "myserver.com") e.preventDefault();
});
```
6. CSP, for example `<meta http-equiv="Content-Security-Policy" content="default-src 'self';">`; redundant with `selfRequestsOnly` but layering is the point. Nonces: `htmx.config.inlineScriptNonce`, `inlineStyleNonce`.
7. CSRF: tokens are a backend job; deliver them with `<body hx-headers='{"X-CSRF-TOKEN": "..."}'>`. With `hx-boost`, body attributes are not replaced, so use an element that is.

## Checked

2026-11-07. Confirmed against the htmx docs Security section (Rule 1, `hx-disable`, `hx-history`, config options, `htmx:validateUrl`, CSP, CSRF) and the hx-disable, hx-history and config reference pages (`selfRequestsOnly`, `allowScriptTags`, `allowEval`, nonce settings and `disableSelector` defaults). Removed an unsourced closing rule about `js:` expressions and the invented Verify step.
Method: documentation only; no commands were run.
