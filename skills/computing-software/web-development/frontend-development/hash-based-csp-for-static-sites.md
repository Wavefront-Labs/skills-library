---
id: computing-software.web-development.frontend-development.hash-based-csp-for-static-sites
name: hash-based-csp-for-static-sites
category: computing-software
field: web-development
product: frontend-development
tags: [content-security-policy, csp, csp-hash, sha256-hash, static-site-csp, meta-csp, inline-script-hash]
level: practitioner
status: docs-checked
description: "Using hash-based CSP for static/cached pages: computing sha256 hashes of inline scripts in the build, strict-dynamic loaders, and meta-tag CSP limits."
sources:
  - https://web.dev/articles/strict-csp
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash-based CSP for static sites

**Goal:** a strict CSP on pages served from a CDN or static host, where per-request nonces are impossible.

## 1. How hashes work
The browser hashes each inline `<script>`'s exact text and runs it only if a matching hash source (`'sha256-<base64>'`, also sha384 or sha512) is in `script-src`. Any change changes the hash. Hashes only cover inline content or external scripts that carry a matching `integrity` attribute.

```bash
# hash an inline script body exactly as it appears between the tags
printf '%s' "$(cat inline.js)" | openssl dgst -sha256 -binary | openssl base64 -A
```
Compute hashes in the build, not by hand.

## 2. Pattern: one hashed loader + strict-dynamic
Hashes only cover inline scripts. External `<script src>` must be loaded by a trusted script under `'strict-dynamic'`:
```html
<script>
  for (const src of ['/assets/app.4f1c.js', '/assets/vendor.9a2b.js']) {
    const s = document.createElement('script'); s.src = src; s.type = 'module'; document.head.append(s);
  }
</script>
```
```
script-src 'sha256-AbC…=' 'strict-dynamic'; object-src 'none'; base-uri 'none'
```
Generate the loader and the header at build time (e.g. Vite/Astro plugins, or a post-build script that hashes and writes `_headers` / a CDN config).

## 3. CSP in a meta tag
`<meta http-equiv="Content-Security-Policy" content="…">` works when you can't set headers (MDN notes it does not support all CSP features): `frame-ancestors`, `report-uri`/`report-to` and `sandbox` are not supported in meta, and a report-only policy cannot be delivered in meta. Put the tag first in `<head>`. Prefer the header.

## 4. External scripts with integrity
Per MDN browser-compat data, matching an external script by its `integrity` hash in `script-src` is supported from Chrome 59, Firefox 116 and Safari 15.6; the loader pattern above works everywhere `strict-dynamic` is supported (Chrome 52, Firefox 52, Safari 15.4).

## Verify
- [ ] Build fails if an inline script's hash is missing from the policy (test in CI by loading pages in headless Chrome and failing on CSP violations).
- [ ] Policy served as a header from the CDN with frame-ancestors.
- [ ] Injected inline script blocked.

## Checked
Checked 2026-10-26 against web.dev strict-csp (updated 2024-09-13: hash policy `script-src 'sha256-...' 'strict-dynamic'` for static or cached pages, third-party scripts loaded by an inline script), MDN CSP guide (meta support limits, report-only not in meta, strict-dynamic passes trust to scripts loaded by a nonced or hashed script) and MDN browser-compat data (script-src external_scripts, strict-dynamic versions). Removed the unconfirmed openssl pipeline remark about console hashes and the 'in some browsers' vagueness. The openssl hashing command was not run.

Method: documentation only; no commands were run.
