---
id: computing-software.devops-ci-cd.verdaccio.webui-branding-and-theme
name: webui-branding-and-theme
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [web-ui, branding, dark-mode, web-title, logo, primary-color, darkmode]
level: practitioner
status: docs-checked
description: "Brand the Verdaccio web UI with title, logo, logoDark, favicon, primaryColor, darkMode, scope, i18n and package sort options; spelling gotchas."
sources:
  - https://verdaccio.org/docs/webui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
web:
  enabled: true
  title: Verdaccio
  logo: /path/to/logo.png
  logoDark: /path/to/logo-dark.png
  favicon: /path/to/favicon.ico
  primaryColor: '#4b5e40'
  darkMode: false
  scope: '@scope'
  sort_packages: asc
  gravatar: true
i18n:
  web: en-US
```
- Logo recommended size is 40x40 pixels. `logoDark` falls back to `logo`.
- `primaryColor` and `scope` must be quoted; `primaryColor` must be valid hex, an invalid value is ignored. Dark theme ignores `primaryColor`.
- `enabled` and `primaryColor` are current; `enable` and `primary_color` are deprecated, and if both colour spellings are set the deprecated one wins, so remove it.
- `darkMode` starts in dark; the choice is stored in the browser's local storage. `showThemeSwitch: false` plus `darkMode` forces one theme.
- `sort_field` (7.x) chooses the sort key (default name).
- `assetFolder` (7.x) serves files under `/-/assets/`, handy with Docker volumes.
- `i18n.web` selects a language from those enabled; default en-US.
- All package access rules also apply to the UI.

## Checked

Confirmed against the Web Configuration page: the YAML options and their defaults, the 40x40 logo size, logoDark fallback, quoting rules for primaryColor and scope, deprecated enable and primary_color spellings and the deprecated colour winning, darkMode with local storage, showThemeSwitch forcing a theme, dark theme ignoring primaryColor, sort_field and assetFolder as 7.x options, i18n default en-US, and access rules applying to the UI. No changes needed.

Method: docs-checked 2026-11-09 against website/docs/web.md in verdaccio/website (source of verdaccio.org/docs/webui/), read in full.
