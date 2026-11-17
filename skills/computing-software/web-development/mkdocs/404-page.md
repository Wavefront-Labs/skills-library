---
id: computing-software.web-development.mkdocs.404-page
name: 404-page
category: computing-software
field: web-development
product: mkdocs
tags: [404-page, not-found, custom-error-page, github-pages]
level: practitioner
status: docs-checked
description: "MkDocs always builds 404.html in the site directory; GitHub Pages uses it only on custom domains, and how to override it in a theme."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every build includes a `404.html` in `site_dir`. Whether a server uses it is a hosting matter:

- GitHub Pages: used automatically only when deploying with a custom domain.
- Other web servers can be configured to use it, but the feature is not always available; check your server's docs.

To change its content, override the template in a theme `custom_dir`:

```yaml
theme:
  name: mkdocs
  custom_dir: custom_theme/
```

and add `custom_theme/404.html`. The 404 page is rendered with the global template context, which is used for HTML pages that do not represent an individual Markdown document, so it has no page-specific context.

## Checked

2026-11-04. Confirmed against Deploying your docs (404 Pages), Customizing Your Theme (overriding `404.html` through `custom_dir`) and the Theme Developer Guide (global context used for `404.html`). Removed: a claim that `page` is `None` and which variables to use, and a generic verify line.

Method: documentation only; no commands were run.
