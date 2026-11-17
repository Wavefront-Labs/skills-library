---
id: computing-software.web-development.mkdocs.local-file-docs
name: local-file-docs
category: computing-software
field: web-development
product: mkdocs
tags: [file-scheme, offline, use-directory-urls, search-plugin]
level: advanced
status: docs-checked
description: "Make a MkDocs site work offline when opened with file:// by setting site_url empty, use_directory_urls false, and dropping the search plugin."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To distribute built files for viewing straight from disk, three settings are needed:

```yaml
site_url: ""
use_directory_urls: false
plugins: []
```

- `site_url: ""` builds the site to work with the `file://` scheme.
- `use_directory_urls: false`, otherwise internal links between pages break.
- Disable the `search` plugin (it does not work on `file://`) or use a third-party search plugin designed for it. `plugins: []` disables all; if you have others, just leave `search` out of the list.

Also:
- All internal links must be relative URLs.
- Modern browser security settings make some features behave differently.
- Many themes load support files from CDNs; offline readers need a theme that bundles them.

Then `mkdocs build` and distribute the `site_dir` contents.

## Checked

2026-11-04. Confirmed against Deploying your docs (Local Files): `site_url` empty string, `use_directory_urls: false`, search plugin disabled or replaced, `plugins: []`, relative internal links, browser security caveat, and CDN themes. Removed: a generic verify line.

Method: documentation only; no commands were run.
