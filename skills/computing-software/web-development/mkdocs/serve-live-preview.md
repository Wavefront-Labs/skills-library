---
id: computing-software.web-development.mkdocs.serve-live-preview
name: serve-live-preview
category: computing-software
field: web-development
product: mkdocs
tags: [mkdocs-serve, live-reload, dev-server, preview]
level: intro
status: docs-checked
description: "Preview a MkDocs site with the built-in dev server and auto-reload; what triggers a rebuild and the default address."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run from the folder containing `mkdocs.yml`:

```bash
mkdocs serve
```

Typical output ends with `Serving on http://127.0.0.1:8000/`. Open that URL in a browser.

The server auto-reloads: it rebuilds when the config file, the documentation directory or the theme directory changes. Edit `docs/index.md` or `site_name` in `mkdocs.yml` and the browser refreshes.

Notes:
- If `site_url` has a path component, serve mounts the site under that path (for example `/foo/`) to mimic the remote layout.
- Hook modules (`hooks:` config) are not reloaded on each build during serve.
- Draft pages (`draft_docs`) appear marked DRAFT in serve; `mkdocs serve --clean` makes serve behave like build.
- Change the address with `dev_addr` or `--dev-addr`.

## Checked

2026-11-04. Confirmed against Getting Started (serve output, `http://127.0.0.1:8000/`, auto-reload on config, docs or theme directory changes) and the configuration guide (site_url mounting, hooks not reloaded, draft_docs and `--clean`, dev_addr). Removed: a generic verify line.

Method: documentation only; no commands were run.
