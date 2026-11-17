---
id: computing-software.web-development.appwrite.appwrite-storage-permissions-file-security
name: appwrite-storage-permissions-file-security
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, storage, permissions, file-security, buckets]
level: practitioner
status: docs-checked
description: "Control file access at bucket level and per file when File security is enabled."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/storage/permissions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide who can read, create, update and delete files.

By default no permissions are granted to any users, so no user can access any files. Permissions are granted, never implied. A user with access granted at either level can access a file; users do not need access at both levels.

- Bucket level: read, create, update or delete permissions on the bucket apply to every file in it. Configure under Your bucket > Settings > Permissions.
- File level: permissions on an individual file, configured on that file. They are only applied if File security is enabled under Your bucket > Settings > File security.

Gotcha: file-level permissions are ignored unless File security is enabled in the bucket settings.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/storage/permissions. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the private-upload pattern with client SDK defaults and the claim that Permission.create() is invalid on files (the page lists create as a file-level permission), the file-token pointer and the invented Verify; kept bucket vs file level, File security setting paths and the no-permissions default.

Method: documentation only; no commands were run.
