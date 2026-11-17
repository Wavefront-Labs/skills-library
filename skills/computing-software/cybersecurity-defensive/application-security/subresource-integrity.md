---
id: computing-software.cybersecurity-defensive.application-security.subresource-integrity
name: subresource-integrity
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [subresource-integrity, sri, third-party-javascript, cdn, security-headers, supply-chain]
level: practitioner
status: docs-checked
description: "Pin third-party scripts and stylesheets with Subresource Integrity: generating hashes, crossorigin requirements, build tooling, what SRI cannot cover, and CSP pairing."
sources: ["https://www.w3.org/TR/SRI/", "https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity", "https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subresource Integrity (SRI)

SRI makes the browser refuse a script or stylesheet whose content does not match a hash you specified. If a CDN
or third-party host is compromised, pinned pages stop loading the altered file instead of running it.

## Usage
```html
<script src="https://cdn.example.com/lib@4.2.1/lib.min.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
        crossorigin="anonymous"></script>
```
- Algorithms: sha256, sha384 (common choice), sha512. Multiple hashes separated by spaces are allowed (the
  strongest supported is used).
- `crossorigin="anonymous"` is required for cross-origin resources, and the host must send CORS headers
  (`Access-Control-Allow-Origin`), otherwise the resource is blocked.

## Generate hashes
```bash
curl -s https://cdn.example.com/lib@4.2.1/lib.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```
Build tooling can also generate `integrity` attributes; check your bundler's documentation.

## Where SRI works and where it does not
- Works: versioned, immutable files (`lib@4.2.1`). Pin exact versions; floating URLs (`/latest/`) change and
  break the page.
- Does not fit: scripts that change by design (tag managers, analytics loaders, ad scripts, payment SDKs that
  vendors update in place). For these: self-host a reviewed copy if licence allows, isolate in an iframe on a
  separate origin, or rely on CSP allowlists plus change monitoring.
- Only covers `<script>` and `<link rel=stylesheet>` (and modulepreload); scripts injected dynamically by other
  scripts are not covered unless the loader sets `integrity`.

## Enforce
- Audit with a crawler or lint rule that every third-party `<script>` has `integrity`.
- Self-hosting first-party assets avoids the issue entirely.

## Verify
Modify one byte of a pinned file in a test environment: the browser console shows an integrity error and the
script does not execute; an automated check lists no third-party script tags without `integrity`.

## Checked
2026-10-28. Confirmed against official pages: integrity attribute, sha256/sha384/sha512, crossorigin and CORS header requirement, script and link coverage (MDN Subresource Integrity; OWASP Third Party JavaScript Management Cheat Sheet).
Removed or rewritten: the polyfill.io incident claim, the shasum alternative, bundler plugin names, and the require-sri-for CSP statement.
Method: documentation only; no commands were run.
