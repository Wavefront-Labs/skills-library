---
id: computing-software.web-development.mkdocs.theme-custom-dir
name: theme-custom-dir
category: computing-software
field: web-development
product: mkdocs
tags: [custom-dir, theme-override, 404-template, parent-theme]
level: practitioner
status: docs-checked
description: "Override files of an existing MkDocs theme with theme.custom_dir: same-name files replace, extra files are added, and name must be an installed theme."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
mkdir custom_theme
```

```yaml
theme:
  name: mkdocs
  custom_dir: custom_theme/
```

Any file in `custom_dir` with the same relative path as a file in the parent theme replaces it; additional files are added. Mirror the parent's structure (templates, JS, CSS, images, fonts).

Examples:
- override the 404 page: add `custom_theme/404.html`
- override the favicon: `custom_theme/img/favicon.ico`
- add a JS library: copy it to `custom_theme/js/` (then link it from a template, see `override-template-blocks`)

Gotchas:
- `theme.name` must be an installed theme. With `name: null` the directory must be a complete standalone theme (see `custom-theme-minimal`).
- Parent files not overridden are still used.
- To remove files or build from scratch, write a custom theme instead.
- `custom_dir` can be relative to the config file or absolute.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Customizing your theme" (Using the theme custom_dir), "Configuration" (theme.custom_dir relative or absolute) and the Developing Themes page. Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
