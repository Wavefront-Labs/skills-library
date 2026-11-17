---
id: computing-software.web-development.mkdocs.site-metadata-copyright
name: site-metadata-copyright
category: computing-software
field: web-development
product: mkdocs
tags: [site-description, site-author, copyright, meta-tags]
level: intro
status: docs-checked
description: "Set MkDocs site_description, site_author and copyright: the first two add meta tags to the HTML header, and the theme includes the copyright text."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
site_name: MkLorum
site_description: Project documentation with Markdown.
site_author: MkDocs Team
copyright: Copyright 2014 Example Author
```

- `site_description`: adds a meta tag to the generated HTML header. Default `null`.
- `site_author`: adds an author meta tag. Default `null`.
- `copyright`: copyright information included by the theme. Default `null`.
- `site_name` is the only required setting; it is also the `site_name` template variable.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (site_name, site_description, site_author, copyright): meta tags in the HTML header, copyright included by the theme, defaults `null`, `site_name` required and passed as a context variable. Removed: a verify line naming a specific meta tag and footer.

Method: documentation only; no commands were run.
