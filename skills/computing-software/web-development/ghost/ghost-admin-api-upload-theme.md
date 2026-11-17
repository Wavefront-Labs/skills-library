---
id: computing-software.web-development.ghost.ghost-admin-api-upload-theme
name: ghost-admin-api-upload-theme
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, theme, zip, upload, deployment, ci]
level: practitioner
status: docs-checked
description: "Deploy a Ghost theme ZIP through the Admin API with a multipart POST, suitable for CI pipelines."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/themes/uploading-a-theme.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/gscan.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: push a theme to a Ghost site without clicking through Ghost Admin.

Send a multipart form request to `/ghost/api/admin/themes/upload` with one field, `file`, containing the theme archive (a Blob or File).

```bash
curl -X POST -F 'file=@/path/to/themes/my-theme.zip' \
  -H "Authorization: Ghost $token" -H "Accept-Version: $version" \
  https://{admin_domain}/ghost/api/admin/themes/upload
```

Pipeline outline:
1. Validate with `gscan -z /path/to/theme.zip` (the `gscan` npm package; see ghost-theme-validation-with-gscan) so fatal errors are caught first.
2. Zip the theme; `index.hbs`, `post.hbs` and `package.json` are the required files.
3. Generate a JWT from the Admin API key.
4. POST the archive.
5. Activate the theme (the endpoint table lists Upload and Activate for `/themes/`).

A theme uploaded in Ghost Admin is checked with gscan automatically and fatal errors prevent it from being used.

Verify: the response describes the uploaded theme and it appears among installed themes in Ghost Admin.

## Checked

2026-11-04. Confirmed: multipart file field, upload path and curl shape, gscan behaviour and CLI forms, required theme files, Upload and Activate in the endpoint table (uploading a theme, gscan, theme structure and Admin API overview pages). Removed: "package.json and index.hbs at the archive root" and the client_max_body_size advice, which no page states.

Method: documentation only; no commands were run.
