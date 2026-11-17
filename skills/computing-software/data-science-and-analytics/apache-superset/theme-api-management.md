---
id: computing-software.data-science-and-analytics.apache-superset.theme-api-management
name: theme-api-management
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [theme-api, ui-theme-administration, themes, rest-api, system-default]
level: advanced
status: docs-checked
description: "Manage Superset themes stored in the database: ENABLE_UI_THEME_ADMINISTRATION, system default and dark themes, and the /api/v1/theme/ REST endpoints."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/theming.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create and switch themes without redeploying (Superset 6.0 or later, which uses Ant Design v5 token theming).

Enable system theme administration in `superset_config.py`:

```python
ENABLE_UI_THEME_ADMINISTRATION = True
```

UI: Settings > Themes, then + Theme. Paste Ant Design theme JSON, name it and save. With the flag on, the sun icon on a theme sets the system default and the moon icon sets the system dark theme; with both set, Superset follows the OS preference. Only administrators with write permissions can change system themes. Removing a designation reverts to configuration-file defaults. Individual dashboards can pick their own theme when edited.

REST endpoints under `/api/v1/theme/`:
- `GET /api/v1/theme/` list; `POST /api/v1/theme/` create
- `PUT /api/v1/theme/{id}` update; `DELETE /api/v1/theme/{id}` delete
- `PUT /api/v1/theme/{id}/set_system_default` and `PUT /api/v1/theme/{id}/set_system_dark` (admin only)
- `DELETE /api/v1/theme/unset_system_default` and `DELETE /api/v1/theme/unset_system_dark`
- `GET /api/v1/theme/export/` (YAML) and `POST /api/v1/theme/import/` (YAML)

The endpoints require appropriate permissions and are subject to RBAC.

Config themes: `THEME_DEFAULT` and `THEME_DARK` in `superset_config.py` use the shape `{"token": {...}}`, with `"algorithm": "dark"` in the dark one. Precedence is: the UI-configured system theme (if the flag is on), then `THEME_DEFAULT` / `THEME_DARK`, then the built-in default. System themes set in the UI can change without a restart. Invalid theme JSON logs a warning and falls back to the built-in default, so check server logs after a change. Setting `THEME_DARK = None` forces a single theme.

## Checked

2026-11-08: read theming.mdx lines 1-162 and 485-512 (frontmatter, UI, config, precedence, API sections). The custom font and example theme sections in between were not read; no claim here depends on them. Removed claims not on the page: bearer-token authentication, version-control and non-default-slot testing advice.
Method: documentation only; no commands were run.
