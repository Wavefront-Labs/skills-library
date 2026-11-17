---
id: computing-software.web-development.hugo.ugly-urls
name: ugly-urls
category: computing-software
field: web-development
product: hugo
tags: [ugly-urls, pretty-urls, html-extension, url-style, per-section]
level: intro
status: docs-checked
description: "Switch Hugo from pretty URLs to ugly .html URLs for the whole site or for chosen sections with the uglyURLs setting."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/ugly-urls.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/output-formats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ugly URLs end in `.html`: `https://example.org/section/article.html`.

Hugo's default is pretty URLs, which omit the file extension: `https://example.org/section/article/`.

Enable ugly URLs for the entire site:

```toml
uglyURLs = true
```

Enable or disable them for specific sections:

```toml
[uglyURLs]
books = true
films = false
```

Output formats have their own switches, both defaulting to `false`: `ugly` enables ugly URLs for that format when the project-level `uglyURLs` is `false`, and `noUgly` disables them for that format when `uglyURLs` is enabled. The docs' Atom feed example sets `noUgly = true` on its custom format (see the custom output formats skill).

## Checked
Confirmed 2026-11-08 against the Hugo ugly URLs and output formats configuration pages (read in full): the examples and defaults are as stated. Made the `ugly` and `noUgly` semantics and defaults precise.
Method: docs-only read of cited pages, 2026-11-08
