---
id: computing-software.data-science-and-analytics.apache-superset.superset-config-file
name: superset-config-file
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [superset-config, configuration, secret-key, locale, hooks]
level: intro
status: docs-checked
description: "Configure Superset via superset_config.py: override path, example settings, D3 locale, chart timing, mutator hooks and asset-creation callbacks."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: override Superset defaults safely.

Override file `superset_config.py`, located via the env var:

```bash
export SUPERSET_CONFIG_PATH=/app/superset_config.py
```

Example keys: `ROW_LIMIT = 5000`, `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `WTF_CSRF_ENABLED = True`, `WTF_CSRF_EXEMPT_LIST = []`, `WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365`, `MAPBOX_API_KEY = ''`. Set at least `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`; alternatively use the `SUPERSET_SECRET_KEY` environment variable.

Locale: `BABEL_DEFAULT_LOCALE = "ru"` and `D3_TIME_FORMAT` (partial overrides such as `months`, `shortMonths`); restart after changes. Language packs are served from `/language_pack/<locale>/<version>/script.js`, non-English only, cached with `max-age=31536000, immutable` for a matching version; `COMMON_BOOTSTRAP_OVERRIDES_FUNC` (`common.language_pack`) takes precedence.

Timing: `CHART_DATA_INCLUDE_TIMING = True` (default `False`) adds `timing.query` with `query_planning_ms`, `cache_resolution_ms`, `data_acquisition_ms`, `payload_assembly_ms`, `total_ms`.

Hooks:
- `FLASK_APP_MUTATOR(app)`, e.g. to set `PERMANENT_SESSION_LIFETIME = timedelta(hours=24)`.
- `AFTER_ASSET_CREATE` (default `None`) is called as `(model, asset_type)` before commit; exceptions abort creation. Skipped for MCP dashboards, copies and imports.
- `EXTRA_ASSET_EXPORT_FIELDS` and `EXTRA_ASSET_IMPORT_HANDLER` (default `None`) carry extra data under the YAML `extra` key.
- `FAB_INDEX_VIEW = "my_overrides.MyIndexView"`: subclass `SupersetIndexView`, and do not set it from `FLASK_APP_MUTATOR`.

Limits: `SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 65535` (warning above 90%).

## Checked

2026-11-08. Confirmed against the Configuring Superset page, read in sections (lines 24-239 and 376-517, plus the OAuth part). Removed: the FEATURE_FLAGS PRESTO_EXPAND_DATA example (not on the page); added the SECRET_KEY and SUPERSET_SECRET_KEY note.
Method: documentation only; no commands were run.
