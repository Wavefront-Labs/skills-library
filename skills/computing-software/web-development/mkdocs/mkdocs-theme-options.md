---
id: computing-software.web-development.mkdocs.mkdocs-theme-options
name: mkdocs-theme-options
category: computing-software
field: web-development
product: mkdocs
tags: [mkdocs-theme, color-mode, nav-style, keyboard-shortcuts]
level: practitioner
status: docs-checked
description: "Configure the built-in mkdocs theme: color_mode, user_color_mode_toggle, nav_style, navigation_depth and keyboard shortcut key codes."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default theme (a custom Bootstrap theme) is selected with `theme.name: mkdocs`. Options:

```yaml
theme:
  name: mkdocs
  color_mode: auto
  user_color_mode_toggle: true
  nav_style: primary
  navigation_depth: 2
  shortcuts:
    help: 191    # ?
    next: 78     # n
    previous: 80 # p
    search: 83   # s
```

- `color_mode`: `light` (default), `dark` or `auto` (follows the device).
- `user_color_mode_toggle` (default `false`): navbar menu letting users pick and persist their mode; initial selection is `color_mode`.
- `nav_style`: `primary` (default), `dark` or `light`; independent of `color_mode`.
- `navigation_depth`: sidebar tree depth, default 2.
- `shortcuts`: all values numeric key codes.
- `locale`: default `en`.

See `mkdocs-theme-highlight-analytics`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Choosing your theme" (mkdocs theme: `color_mode`, `user_color_mode_toggle`, `nav_style`, `navigation_depth`, `shortcuts` defaults and key codes, `locale`). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
