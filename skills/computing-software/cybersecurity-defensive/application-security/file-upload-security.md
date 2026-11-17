---
id: computing-software.cybersecurity-defensive.application-security.file-upload-security
name: file-upload-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, file-upload-security, unrestricted-file-upload, content-type-validation, malware-scanning, path-traversal]
level: advanced
status: docs-checked
description: "Secure file uploads: allow-list extensions and verify content, rename and store outside the web root, cap size, scan for malware and serve with safe headers."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File upload security

**Goal:** uploads can never become executable code, overwrite files, exhaust storage or deliver malware to other users.

## Controls
1. **Allow-list extensions** for the business need (`.pdf, .png, .jpg`); compare lower-cased final extension, reject double extensions like `x.php.jpg` handled by misconfigured servers.
2. **Verify content**: check the file signature; for images, re-encode (decode and re-save) to strip polyglots and metadata. Do not trust the client `Content-Type`.
3. **Generate the stored name** (UUID); keep the original name only as metadata, sanitised. Prevents path traversal (`../../etc/cron.d/x`) and overwrites.
4. **Store outside the web root**, ideally object storage with no public access; serve through an app endpoint or short-lived signed URLs.
5. **Size limits** at proxy, app, and per-user quotas; limit decompressed size for archives (zip bombs) and reject archive entries with `..` (zip slip).
6. **Malware scanning** before files are made available (antivirus or a sandbox); quarantine on detection.
7. **Serve safely**: `Content-Disposition: attachment` for non-images, `X-Content-Type-Options: nosniff`, correct `Content-Type`, and ideally a separate sandbox domain for user content.

## Special types
- SVG contains script: serve as attachment or sanitise; never inline on the main origin.
- Office documents with macros and PDFs with JavaScript: scan, or convert (CDR) if high risk.
- XML-based formats (DOCX, XLSX, SVG): parse with XXE disabled.

## Gotchas
- Checking extension only on the client side.
- Writing to a temp dir under the web root before validation.
- Image-processing libraries have had remote code execution bugs; keep them updated and restrict what they may process.

## Verify
- [ ] Uploading `shell.php`, `shell.php.jpg`, a renamed EXE and an EICAR file are each rejected or quarantined.
- [ ] Stored object keys are random; files are not reachable by guessing the original name.

## Checked
2026-10-28. Confirmed against official pages: extension allow-list, file-signature checks, generated filenames, size limits, antivirus/sandbox scanning and CDR (OWASP File Upload Cheat Sheet).
Removed or rewritten: tool and product names (file, python-magic, Tika, ClamAV, GuardDuty, Defender), the nginx directive, ImageMagick policy.xml, and the CWE and WSTG sources (not fetched).
Method: documentation only; no commands were run.
