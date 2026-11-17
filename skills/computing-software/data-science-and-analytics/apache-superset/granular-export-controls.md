---
id: computing-software.data-science-and-analytics.apache-superset.granular-export-controls
name: granular-export-controls
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [granular-export-controls, can-export-data, can-export-image, can-copy-clipboard, permissions]
level: practitioner
status: docs-checked
description: "Separate Superset export rights with GRANULAR_EXPORT_CONTROLS: can_export_data, can_export_image and can_copy_clipboard, migration and API enforcement."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/security/granular-export-controls.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a role view charts without taking the data out.

Three permissions, all on the `Superset` resource, replace the legacy `can_csv` permission and can be assigned independently:
- `can_export_data`: CSV, Excel and JSON data exports from charts, dashboards and SQL Lab.
- `can_export_image`: screenshot (JPEG/PNG) and PDF exports from charts and dashboards.
- `can_copy_clipboard`: copy-to-clipboard in SQL Lab and the Explore data pane.

They are gated behind the feature flag; with it disabled, legacy `can_csv` behaviour is preserved:

```python
FEATURE_FLAGS = {"GRANULAR_EXPORT_CONTROLS": True}
```

Steps:

```bash
superset db upgrade
superset init
```

`db upgrade` registers the new permissions and `init` populates roles. The migration grants all three permissions to every role that currently has `can_csv`, so no role loses access. Verify roles in Settings > List Roles, then revoke individual permissions in the role editor. Example from the docs: to stop Gamma users exporting data or images but keep clipboard copy, revoke `can_export_data` and `can_export_image` from Gamma.

User experience without a permission: export menu items and buttons appear disabled with a tooltip, and API endpoints return 403 Forbidden.

API endpoints enforcing it when the flag is on:
- `GET /api/v1/chart/{id}/data/` (CSV/Excel format): `can_export_data`
- `GET /api/v1/chart/{id}/cache_screenshot/`: `can_export_image`
- `POST /api/v1/dashboard/{id}/cache_dashboard_screenshot/`: `can_export_image`
- `GET /api/v1/sqllab/export/{client_id}/`: `can_export_data`
- `POST /api/v1/sqllab/export_streaming/`: `can_export_data`

## Checked

2026-11-08: read granular-export-controls.mdx in full. Removed claims not on the page: embedded-dashboard and restricted-role testing advice.
Method: documentation only; no commands were run.
