---
id: computing-software.web-development.appwrite.appwrite-storage-buckets-settings
name: appwrite-storage-buckets-settings
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, storage, buckets, compression, encryption, cli]
level: intro
status: docs-checked
description: "Create storage buckets and configure permissions, file security, encryption, compression, size limits and allowed extensions in the Console or CLI."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/storage/buckets/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up a bucket that stores files safely.

Create: Console > Storage > Create bucket, a Server SDK (`storage.createBucket`), or the CLI: `appwrite init buckets` writes the bucket into `appwrite.config.json` and `appwrite push buckets` creates it in the Console.

Settings the docs describe:
- Permissions: see the storage permissions skill.
- Encryption: Settings > Security settings; files larger than 20MB cannot be encrypted.
- Compression: Settings > Compression; gzip or zstd; skipped for files larger than 20MB even when enabled.
- Maximum file size: Settings > Maximum file size.
- File extensions: Settings > File extensions; up to 100 extensions, blank allows all types.

Pick compression and encryption deliberately: both are skipped above 20MB, so large media does not get either protection.

Gotcha: a new bucket grants no permissions by default, so users cannot create or read files until you add permissions.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/storage/buckets. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the antivirus line and the file-security setting (neither is on the Buckets page); Gotcha reworded to the page (no permissions granted by default, so users cannot create or read files) without the unverified Role.users() example; removed the invented Verify; settings locations added.

Method: documentation only; no commands were run.
