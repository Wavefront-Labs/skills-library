---
id: computing-software.web-development.directus.asset-url-access
name: asset-url-access
category: computing-software
field: web-development
product: directus
tags: [asset-url, import-file-url, assets-endpoint, file-access-token]
level: intro
status: docs-checked
description: "Import a file into Directus by URL in the Files module and serve it from /assets/<file-id> with an access_token unless public read is allowed."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/6.upload-files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Import: open the Files module in the module bar, click the add button, then the link icon, and give any publicly accessible image URL. The file lands in your asset storage and can be downloaded, edited or replaced in the Studio by users with access.

Serve it in an app with:

```
https://example.directus.app/assets/<file-id>?access_token=token
```

Rules:
- The token must belong to a user with read access to the `directus_files` collection.
- If the public role has read access on files, omit `access_token`.

## Checked

2026-11-04: import by URL steps, storage, Studio access, the /assets URL pattern, token requirement and public role exception confirmed against the Directus Upload & Access Files page. Removed a claim about finding the file id on the detail page and a Verify line, neither stated in the page text.

Method: documentation only; no commands were run.

Related: image resizing via query parameters is covered in the image transform skill.
