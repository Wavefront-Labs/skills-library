---
id: computing-software.web-development.mkdocs.override-template-blocks
name: override-template-blocks
category: computing-software
field: web-development
product: mkdocs
tags: [template-blocks, main-html, jinja2, super-block]
level: advanced
status: docs-checked
description: "Override named Jinja blocks of the mkdocs or readthedocs theme from a custom main.html, and use super() to add scripts without dropping the parent's."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `custom_dir`, create `main.html` that extends `base.html` and redefines blocks:

```django
{% extends "base.html" %}

{% block htmltitle %}
<title>Custom title goes here</title>
{% endblock %}
```

Blocks in the mkdocs and readthedocs themes: `site_meta`, `htmltitle`, `styles`, `libs`, `scripts`, `analytics`, `extrahead` (empty, for custom head tags), `site_name`, `site_nav`, `search_button`, `next_prev`, `repo`, `content`, `footer`.

A new block replaces the parent's wholesale. To add a library to `libs` and keep the existing ones, call `super()`:

```django
{% extends "base.html" %}

{% block libs %}
    {{ super() }}
    <script src="{{ base_url }}/js/somelib.js"></script>
{% endblock %}
```

Use `base_url` so the link is relative to the current page. Copy the file into `custom_theme/js/somelib.js`. The same applies to extra CSS.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Customizing your theme" (Overriding Template Blocks; Combining the custom_dir and Template Blocks), including the list of blocks and the `super()` example. Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
