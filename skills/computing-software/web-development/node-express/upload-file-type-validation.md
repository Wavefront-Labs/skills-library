---
id: computing-software.web-development.node-express.upload-file-type-validation
name: upload-file-type-validation
category: computing-software
field: web-development
product: node-express
tags: [file-upload-security, secure-file-upload, file-type-validation, magic-bytes, content-type-sniffing, extension-allowlist, file-type, owasp-file-upload]
level: practitioner
status: verified
description: "Validating uploaded files server-side: extension allowlists, magic-byte detection, not trusting client Content-Type, SVG/HTML risks and safe serving headers."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://github.com/sindresorhus/file-type
  - https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload file type validation

**Goal:** only the file types you intend are accepted, and nothing uploaded can execute in your origin or on your server.

## 1. Trust nothing the client sends
`originalname`, its extension and the multipart `Content-Type` are attacker-controlled. Validate:
1. **Extension allowlist** (lowercased, last extension only, after stripping): `.jpg .jpeg .png .webp .pdf`.
2. **Magic bytes** match an allowed type:
```js
import { fileTypeFromBuffer } from 'file-type';
const ft = await fileTypeFromBuffer(buf.subarray(0, 4100));   // 4100 bytes is file-type's default sample size
if (!ft || !['image/jpeg','image/png','image/webp','application/pdf'].includes(ft.mime)) throw badRequest('unsupported file');
```
3. For images, actually decode them (sharp/libvips) - polyglot files pass magic-byte checks; re-encoding destroys appended payloads (see re-encoding skill). Run with file-type and sharp: real PNG, JPEG, WebP and PDF bytes were detected, an HTML file and an SVG returned no type (rejected), and a PNG with `<script>` appended was still detected as `image/png` but the `sharp(...).png()` output no longer contained the script.

## 2. Dangerous types
- **SVG**: is XML with script - serving it inline from your origin is stored XSS (a Chromium 156 test ran the script of a directly opened `image/svg+xml` response; with `Content-Security-Policy: default-src 'none'; sandbox` it did not run). Reject, sanitize (DOMPurify server-side with SVG profile), or rasterize.
- **HTML/XHTML/XML, .js, .swf**: never accept for user content.
- **Office/PDF**: may contain macros/JS; serve as downloads; scan with AV (ClamAV) for user-to-user sharing.
- Archives: zip bombs and zip slip (see size limits and path traversal skills).

## 3. Serving uploads safely
- From a **separate domain** (`usercontent.example-cdn.com`) or object storage, never your app origin, so any script runs in a cookieless origin.
- `Content-Type` set by you from the validated type; `X-Content-Type-Options: nosniff` (a `text/plain` response containing HTML did not execute in Chromium 156, with or without it, so treat nosniff as defence in depth); `Content-Disposition: attachment; filename="…"` for anything not meant to display inline; `Content-Security-Policy: default-src 'none'; sandbox` on the upload host.

## 4. Never execute
Store outside any directory the web server interprets (no `.php` handler, no `public/` in Rails/Express static). Generate the stored filename yourself.

## Verify
- [ ] Upload a `.jpg` that is really HTML: rejected.
- [ ] Upload `x.svg` with `<script>`: rejected or sanitized; opening the stored URL doesn't execute script.
- [ ] Response headers on served files include nosniff and the forced content type.
