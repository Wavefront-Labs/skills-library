---
id: computing-software.web-development.mkdocs.site-url-canonical
name: site-url-canonical
category: computing-software
field: web-development
product: mkdocs
tags: [site-url, canonical-url, subdirectory-hosting, mkdocs-serve]
level: practitioner
status: docs-checked
description: "Set site_url for MkDocs: canonical link tags, subdirectory hosting, how serve mounts the site, and the empty-string value for file:// use."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
site_url: https://example.com/foo/
```

Effects (default `null`):
- Adds a `link rel=canonical` tag to the `head` of every page.
- If the site root is in a subdirectory of the domain, include the subdirectory (`https://example.com/foo/`).
- `mkdocs serve` mounts the site at the path component of the URL, so `some/page.md` is served from `http://127.0.0.1:8000/foo/some/page/`.
- Nav items with relative URLs like `'../'` step up from this subdirectory.

For documentation distributed as local files (`file://`), set it to an empty string:

```yaml
site_url: ""
```

Setting the subdirectory also changes the path used by local `mkdocs serve`, as above.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (site_url, nav examples) and Deploying your docs (Local Files: `site_url` must be an empty string for `file://`). Removed: a gotcha about forgotten subdirectories and a generic verify line.

Method: documentation only; no commands were run.
