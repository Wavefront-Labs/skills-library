---
id: computing-software.web-development.mkdocs.use-directory-urls
name: use-directory-urls
category: computing-software
field: web-development
product: mkdocs
tags: [use-directory-urls, pretty-urls, s3-hosting, file-urls]
level: practitioner
status: docs-checked
description: "Choose between folder-style URLs and .html file URLs with use_directory_urls, and when false is required (file system, static S3)."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default is `true`: friendlier URLs.

| Source | Generated file | URL |
| --- | --- | --- |
| index.md | /index.html | / |
| api-guide.md | /api-guide/index.html | /api-guide/ |
| about/license.md | /about/license/index.html | /about/license/ |

Set `false` for hosts that cannot serve `X/index.html` for the URL `X`:

```yaml
use_directory_urls: false
```

Then `api-guide.md` becomes `api-guide.html` with links pointing at the file, and no extra directory is made.

Required `false` for:
- opening pages directly from the file system
- publishing to a static S3 website

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Configuration" (use_directory_urls: both tables, the two cases needing `false`, default `true`). Removed the file:// gotcha and the Verify line, which the page does not state.
Method: documentation only; no commands were run.
