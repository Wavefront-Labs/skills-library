---
id: computing-software.web-development.frontend-development.subresource-integrity
name: subresource-integrity
category: computing-software
field: web-development
product: frontend-development
tags: [security-headers, http-security-headers, subresource-integrity, sri, integrity-attribute, crossorigin-attribute, third-party-scripts, supply-chain]
level: practitioner
status: docs-checked
description: "Pinning third-party scripts and styles with Subresource Integrity: generating hashes, crossorigin requirements, version pinning and what SRI can't protect."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/crossorigin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subresource Integrity (SRI)

**Goal:** a compromised CDN or package host can't swap the JavaScript/CSS your pages load.

## 1. Add integrity
```html
<script src="https://cdn.example.com/lib@1.2.3/lib.min.js"
        integrity="sha384-<base64-hash>" crossorigin="anonymous"></script>
```
Generate:
```bash
curl -s URL | openssl dgst -sha384 -binary | openssl base64 -A
```
The browser hashes the response and refuses to execute it on mismatch (console error, `error` event on the element).

## 2. Requirements
- Cross-origin resources need `crossorigin="anonymous"` and the server must send `Access-Control-Allow-Origin`: SRI requires CORS, and browsers refuse SRI on `no-cors` requests.
- **Pin exact versions**. `@latest` or unversioned URLs change content and break SRI on the next release.
- The `integrity` value is a whitespace-separated list of `sha256-`, `sha384-` or `sha512-` hashes. MDN: the browser uses only the hashes of the strongest algorithm present and ignores the others; several hashes of the same algorithm let you offer alternate versions of a resource.

## 3. Bundled apps
Bundlers and plugins can add SRI to emitted `<script>`/`<link>` tags; useful when assets come from a separate CDN origin. For module graphs, an import map can carry an `integrity` key that maps module URLs to integrity metadata for statically or dynamically imported modules (MDN, importmap page).

## 4. What SRI doesn't cover
- Scripts that load **other** scripts at runtime (tag managers, analytics, chat widgets) - SRI only checks the first file; files that change continuously can't be SRI-pinned. Self-host or sandbox them (iframe) and rely on CSP.
- Fonts/images: MDN lists SRI for `<script>` and `<link>` elements whose `rel` is `stylesheet`, `preload` or `modulepreload`.

## 5. Failure handling
SRI mismatch = the script doesn't run. For critical libraries, self-host instead of building fallback chains.

## Verify
- [ ] Changing one byte in a locally served copy (or a wrong hash) blocks execution with an integrity error.
- [ ] All third-party `<script src>` tags either have integrity or are documented exceptions.
- [ ] Enforcement is by review or linting of the HTML/build output.

## Checked
Checked 2026-10-26 against MDN Subresource Integrity (allowed hash prefixes sha256/sha384/sha512, strongest-algorithm rule, CORS requirement, no-cors refused, element list script/link with stylesheet/preload/modulepreload) and the MDN importmap page (integrity key for module integrity metadata). Replaced the pinned CDN example with a placeholder URL and removed unconfirmed items: bundler plugin names, the require-sri-for remark and the legacy document.write fallback remark. The curl and openssl hash command was not run.

Method: documentation only; no commands were run.
