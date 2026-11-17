---
id: computing-software.web-development.mkdocs.build-site
name: build-site
category: computing-software
field: web-development
product: mkdocs
tags: [mkdocs-build, site-directory, gitignore, cli-help]
level: intro
status: docs-checked
description: "Build the static site with mkdocs build, inspect the site directory output, ignore it in git, and discover other commands with --help."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
mkdocs build
```

Output goes to `site/` (the `site_dir` default). Each page `about.md` becomes `about/index.html`, theme assets are copied in, and you also get `sitemap.xml` and a search index JSON file (the tutorial lists `mkdocs/search_index.json`).

The build is static, so any host that serves files can serve it. Do not commit build output:

```bash
echo "site/" >> .gitignore
```

Discover commands and options:

```bash
mkdocs --help
mkdocs build --help
```

Use `-f`/`--config-file` for a non-default config path and `--strict` to turn warnings into failures.

## Checked

2026-11-04. Confirmed against Getting Started (Building the site, Other Commands and Options) and the configuration guide (site_dir, strict): `site/` output, `about/index.html`, `sitemap.xml`, `mkdocs/search_index.json`, the `.gitignore` line, `--help`, `--strict` and `-f`/`--config-file`. Removed: a generic verify line.

Method: documentation only; no commands were run.
