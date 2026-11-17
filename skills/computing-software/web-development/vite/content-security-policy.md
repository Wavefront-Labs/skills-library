---
id: computing-software.web-development.vite.content-security-policy
name: content-security-policy
category: computing-software
field: web-development
product: vite
tags: [csp-nonce, html-csp-nonce, data-uri-csp]
level: advanced
status: docs-checked
description: "Deploy a CSP with Vite: html.cspNonce adds nonces and a csp-nonce meta tag, and data: must be allowed for img and font (never script) or assetsInlineLimit set to 0."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nonce: when `html.cspNonce` is set, Vite adds a `nonce` attribute with that value to `<script>` and `<style>` tags, and to `<link>` tags for stylesheets and module preloading. It also injects:

```html
<meta property="csp-nonce" nonce="PLACEHOLDER" />
```

Vite uses that meta tag's nonce whenever needed, in dev and after build. Replace the placeholder with a unique value on every request, otherwise the policy is easy to bypass.

`data:`: by default builds inline small assets as data URIs. Either allow `data:` in related directives (for example `img-src`, `font-src`) or disable inlining:

```js
export default { build: { assetsInlineLimit: 0 } }
```

Never allow `data:` for `script-src`; it permits injecting arbitrary scripts.

## Checked

Date: 2026-11-07. Read the CSP section of features.md (features.md read in full), the `html.cspNonce` section of shared-options.md (read in full) and `build.assetsInlineLimit` in build-options.md (read in full). The nonce targets, injected `csp-nonce` meta tag, per-request placeholder warning, `data:` handling and the `script-src` warning matched; nothing trimmed.

Method: documentation only; no commands were run.
