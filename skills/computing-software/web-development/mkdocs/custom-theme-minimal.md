---
id: computing-software.web-development.mkdocs.custom-theme-minimal
name: custom-theme-minimal
category: computing-software
field: web-development
product: mkdocs
tags: [custom-theme, main-html, jinja2, theme-files]
level: advanced
status: docs-checked
description: "Build a minimal custom MkDocs theme: main.html Jinja2 template outside docs_dir, name: null, CSS/JS tags, and which theme files are copied or ignored."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minimum: a `main.html` Jinja2 template in a directory that is not inside `docs_dir`.

```yaml
theme:
  name: null
  custom_dir: 'custom_theme/'
```

```django
<!DOCTYPE html>
<html>
  <head>
    <title>{% if page.title %}{{ page.title }} - {% endif %}{{ config.site_name }}</title>
    {%- for path in config.extra_css %}
      <link href="{{ path | url }}" rel="stylesheet">
    {%- endfor %}
  </head>
  <body>
    {{ page.content }}
    {%- for script in config.extra_javascript %}
      {{ script | script_tag }}
    {%- endfor %}
  </body>
</html>
```

Rules:
- The theme must render `extra_css`/`extra_javascript` or those options do nothing. Use `config.extra_javascript` and `script_tag` (1.5+).
- `.html` files are templates, not copied; other files are copied as-is. A same-path file in `docs_dir` wins.
- Ignored: `mkdocs_theme.yml`, Python files, dot-prefixed names, Markdown and README files.
- With `name: null`, all theme config must be in `mkdocs.yml` (no `mkdocs_theme.yml` is read from `custom_dir`).

Tip: the mkdocs-basic-theme repository is a commented starting point.

## Checked

2026-11-04. Confirmed against the MkDocs Developing Themes page (Creating a custom theme; Basic theme; Picking up CSS and JavaScript from the config; Theme Files: template files, theme meta files, dot files, documentation files). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
