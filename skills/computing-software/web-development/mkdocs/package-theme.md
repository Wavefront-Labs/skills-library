---
id: computing-software.web-development.mkdocs.package-theme
name: package-theme
category: computing-software
field: web-development
product: mkdocs
tags: [package-theme, entry-points, mkdocs-theme-yml, extends]
level: advanced
status: docs-checked
description: "Package a MkDocs theme for pip: layout, MANIFEST.in, setup.py mkdocs.themes entry point, the required mkdocs_theme.yml and its special options."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Packaging is optional for one-off themes (a `custom_dir` suffices) but gives users pip install, default config and the ability to tweak via `custom_dir`.

Layout:

```text
.
|-- MANIFEST.in
|-- theme_name
|   |-- __init__.py        # empty, marks the package
|   |-- mkdocs_theme.yml   # required, may be blank
|   |-- main.html
|   |-- styles.css
`-- setup.py
```

`MANIFEST.in`:

```text
recursive-include theme_name *.ico *.js *.css *.png *.html *.eot *.svg *.ttf *.woff
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

In `setup.py`: `include_package_data=True` and

```python
entry_points={'mkdocs.themes': ['themename = theme_name']}
```

Name the package `mkdocs-themename`. The left side is what users put in `theme.name`.

`mkdocs_theme.yml` holds defaults. Special options: `locale` (default `en`), `static_templates` (users can add, not remove), `extends` (parent theme name).

## Checked

2026-11-04. Confirmed against the MkDocs Developing Themes page (Packaging Themes: Package Layout, MANIFEST.in, setup.py entry point, Theme Configuration special options). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
