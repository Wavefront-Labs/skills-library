---
id: computing-software.web-development.appwrite.appwrite-storage-file-tokens
name: appwrite-storage-file-tokens
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, storage, file-tokens, sharing, server-sdk]
level: advanced
status: docs-checked
description: "Share files publicly through view, preview or download URLs protected by revocable file tokens with optional expiry."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/storage/file-tokens/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give outsiders access to specific files without configuring bucket or file permissions.

A file token is a secret that lets anyone with it access a file without a session. It can expire on a specific date or work indefinitely. Tokens avoid the third-party cookie problem, because they do not depend on the session for authorization.

Console: Storage > open a file in a bucket > File tokens section > Create file token. The three-dots menu offers Copy URL (token-based preview, view and download URLs), Edit expiry and Delete.

Server SDK (`Tokens` service): needs an API key with the `tokens.write` scope to create (`createFileToken(bucketId, fileId, expire)`), update expiry (`update(tokenId, expire)`) or delete (`delete(tokenId)`), and `tokens.read` to list (`list(bucketId, fileId)`) or get (`get(tokenId)`). Listing shows expiry dates and when each token was last accessed. The expiry is set at creation and can be updated later.

The token is used with the storage view, preview and download endpoints.

Gotcha: a token with no expiry works indefinitely; set an expiry for temporary shares.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/storage/file-tokens. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the claim that preview tokens combine with transformation parameters, "limit exposure to one file", "revoke immediately", the treat-it-like-a-password Gotcha and the invented Verify; added what the page states (no bucket or file permission needed, third-party cookie background, list shows expiry and last access, Console steps).

Method: documentation only; no commands were run.
