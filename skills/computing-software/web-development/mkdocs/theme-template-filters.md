---
id: computing-software.web-development.mkdocs.theme-template-filters
name: theme-template-filters
category: computing-software
field: web-development
product: mkdocs
tags: [template-filters, template-variables, jinja2, nav-template]
level: advanced
status: docs-checked
description: "Use MkDocs theme template variables (config, nav, page, base_url, pages) and the url, tojson and script_tag filters in Jinja2 templates."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global variables in every template: `config` (the loaded mkdocs.yml), `nav`, `base_url`, `mkdocs_version`, `build_date_utc`, `pages` (flat list of all `File` objects; page via `file.page`) and `page`. For templates not rendered from Markdown (404.html, search.html) `page` is `None`.

Filters:
- `url`: absolute URLs untouched; a relative URL is made relative to the page when the context has a page object, otherwise `base_url` is prepended.
- `tojson`: safely embed a Python object in JavaScript.
- `script_tag` (1.5+): turns an `extra_javascript` item into a `<script>` tag honouring type/async/defer.

```django
<a href="{{ page.url|url }}">{{ page.title }}</a>
<script>var mkdocs_page_name = {{ page.title|tojson|safe }};</script>
```

Nav loop:

```django
{% for nav_item in nav %}
  <a href="{{ nav_item.url|url }}">{{ nav_item.title }}</a>
{% endfor %}
```

Page attributes include `title`, `content`, `toc`, `meta`, `url`, `abs_url`, `canonical_url`, `edit_url`, `is_homepage`, `previous_page`, `next_page`, `active`. Navigation items are sections, pages or links; sections have no URL.

Pass custom values with `extra` and read `config.extra.version`.

## Checked

2026-11-04. Confirmed against the MkDocs Developing Themes page (Template Variables: config, nav, base_url, mkdocs_version, build_date_utc, pages, page attributes, navigation objects, Extra Context; Template Filters: url, tojson, script_tag). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
