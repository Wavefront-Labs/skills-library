---
id: computing-software.data-science-and-analytics.apache-superset.theming-configuration
name: theming-configuration
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [theming, theme-default, theme-dark, ant-design-tokens, fonts]
level: practitioner
status: docs-checked
description: "Customise Superset 6.0+ appearance: THEME_DEFAULT, THEME_DARK, THEME_DEFAULT_MODE, Ant Design v5 tokens, fontUrls allowlist and ECharts overrides."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/theming.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply brand colours, fonts and dark mode (apache-superset 6.0 or later; theming uses Ant Design v5 tokens).

```python
ENABLE_UI_THEME_ADMINISTRATION = True   # optional

THEME_DEFAULT = {"token": {"colorPrimary": "#2893B3"}}
THEME_DARK = {"algorithm": "dark", "token": {"colorPrimary": "#2893B3"}}
THEME_DEFAULT_MODE = "system"
```

- `THEME_DEFAULT` and `THEME_DARK` seed the light and dark themes. Set `THEME_DARK = None` to force a single theme. With both defined, users can switch and OS preference detection is on.
- `THEME_DEFAULT_MODE` is the starting mode for sessions with no saved preference: `"default"` (always light), `"dark"` or `"system"` (follow the OS, the default; needs a dark theme). A user's saved choice wins, and it has no effect on embedded dashboards (the embed SDK `themeMode` URL parameter decides).
- With `ENABLE_UI_THEME_ADMINISTRATION = True`, admins manage themes under Settings, Themes: create from Ant Design Theme Editor JSON, set the system default (sun icon) or system dark (moon icon) theme without a restart, and assign a theme per dashboard. UI system themes take precedence over config themes, then `THEME_DEFAULT`/`THEME_DARK`, then the built-in theme. Invalid theme JSON is logged as a warning and falls back.
- Branding: the `brandAppName` token sets the app name (it beats `APP_NAME`); `HIDE_NAVBAR_LOGO = True` hides the navbar brand area (config flag, not a token).

Fonts: Inter is the default UI font and IBM Plex Mono the code font, both bundled. For custom fonts put URLs in the `fontUrls` token and reference them in `fontFamily` and `fontFamilyCode`; also widen the CSP (`font-src`, `style-src` in `TALISMAN_CONFIG`). Font URLs are checked against an allowlist: by default `fonts.googleapis.com`, `fonts.gstatic.com` and `use.typekit.net`; change it with `THEME_FONT_URL_ALLOWED_DOMAINS`.

Charts: `echartsOptionsOverrides` applies to all ECharts charts and `echartsOptionsOverridesByChartType` (keys such as `echarts_pie`, `echarts_timeseries`) to one type. Later wins: base theme, plugin options, global overrides, chart-type overrides. Objects deep-merge but arrays are replaced entirely.

Theme REST API: `/api/v1/theme/` (list, create), `/api/v1/theme/{id}` (update, delete), `set_system_default` and `set_system_dark` (admin only), `export/` and `import/` as YAML.

## Checked

2026-11-08. Confirmed against the Theming page (read in full). Removed: the claim that THEME_DEFAULT_MODE takes only "default" (the page lists three values), the unsourced "restart and clear browser cache" advice, and the description of fonts loaded "through a theme font URL" (the token is `fontUrls`). Component sizing tokens are marked master-only on the page and were left out.
Method: documentation only; no commands were run.
