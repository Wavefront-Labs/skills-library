---
id: computing-software.web-development.node-express.serving-user-content-from-a-sandbox-domain
name: serving-user-content-from-a-sandbox-domain
category: computing-software
field: web-development
product: node-express
tags: [user-content-domain, svg-xss, sandbox-domain, public-suffix-list, csp-sandbox, file-upload-security]
level: advanced
status: draft
description: "Isolating user-uploaded content: separate registrable domain, CSP sandbox and attachment headers, safe handling of SVG/HTML uploads, signed URLs and per-user subdomains."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://github.blog/engineering/githubs-csp-journey/
  - https://publicsuffix.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serving user content from a sandbox domain

Any user upload that a browser can render as HTML or SVG runs script in the origin that serves it. If that origin is your app, the uploader has stored XSS.

## 1. Separate registrable domain
- Serve uploads from `example-usercontent.com` (a different eTLD+1), not `files.example.com`. Subdomains share cookies scoped to `.example.com` and count as same-site (SameSite cookies and CSRF defences treat them as trusted).
- Per-user/tenant subdomains (`alice.example-pages.com`) need the domain on the **Public Suffix List** so each subdomain is its own site.
- Examples: GitHub (`githubusercontent.com`), Google (`googleusercontent.com`).

## 2. Headers on every user-content response
```http
Content-Type: <type detected server-side, never the client's>
X-Content-Type-Options: nosniff
Content-Disposition: attachment; filename="..."          (inline only for allowlisted image/video types)
Content-Security-Policy: sandbox; default-src 'none'; img-src 'self'; style-src 'unsafe-inline'
Cross-Origin-Resource-Policy: cross-origin               (or same-site if only your app embeds them)
```
`CSP: sandbox` gives the document an opaque origin with scripts disabled even if it is rendered.

## 3. SVG and HTML uploads
- SVG can contain `<script>`, event handlers and `<foreignObject>`. Options: rasterise to PNG on upload (safest), sanitise with DOMPurify's SVG profile, or serve only as `attachment`/via `<img>` (scripts do not run in `<img>`-loaded SVG, but direct navigation does).
- HTML uploads: never inline on any domain you care about; attachment only or render in a sandboxed iframe from the sandbox domain (`<iframe sandbox src="https://example-usercontent.com/...">`).

## 4. Access control
Private files via short-lived signed URLs (S3/GCS presigned GET, CloudFront signed URLs) tied to the requesting user; never long-lived public object URLs for private data.

## Verify
- [ ] Uploading `<svg onload=alert(document.domain)>` and opening its URL directly shows the sandbox domain (or no execution), never your app's domain.
- [ ] App cookies are absent from requests to the content domain.
