---
id: computing-software.data-science-and-analytics.apache-superset.dashboard-excel-export
name: dashboard-excel-export
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [excel-export, export-storage, dashboard-export, can-export, data-export]
level: practitioner
status: docs-checked
description: "Export dashboard data to Excel in Superset: direct versus EXPORT_STORAGE background path, row limit, link TTL, extras and image export prerequisites."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/using-superset/exporting-dashboard-data.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let users download every chart of a dashboard as one Excel workbook (one worksheet per chart, respecting the active filters).

Use: dashboard ... (actions), Download, Export Data to Excel. The action appears for users with the dashboard `can_export` permission. Export Images to Excel embeds rendered images for non-table charts and needs export storage plus the headless webdriver with the `ENABLE_DASHBOARD_SCREENSHOT_ENDPOINTS` and `ENABLE_DASHBOARD_DOWNLOAD_WEBDRIVER_SCREENSHOT` feature flags.

Two paths:
- Direct download (default, no configuration): the workbook is built during the request. The combined `row_limit` of its queries must not exceed `EXCEL_EXPORT_SYNC_MAX_ROWS` (default 100000; keep it within your web server request timeout). Charts whose size cannot be known (for example pivot tables with AVG or COUNT DISTINCT, or post-processing that adds rows) are skipped and listed on an Export Summary sheet.
- Background path for larger exports and all image exports: set `EXPORT_STORAGE` with both a bucket and a backend (no implicit default), for example `{"bucket": "my-export-bucket", "backend": S3ExportStorage()}` from `superset.utils.s3` (or `GCSExportStorage` from `superset.utils.gcs`). Optional `key_prefix` defaults to `"dashboard-exports/"`. It needs the SDK on web and worker tiers (`pip install apache-superset[excel-export]` for S3, `apache-superset[excel-export-gcs]` for GCS) and a running Celery worker; deployments overriding `CELERY_CONFIG` must add `superset.tasks.export_dashboard_excel` to `imports`. `EXCEL_EXPORT_SYNC_MAX_ROWS` is ignored when storage is set.

Links: `EXCEL_EXPORT_LINK_TTL_SECONDS` (default 86400) is the lifetime of the Superset download link sent by email (SMTP settings as for alerts and reports) and returned to the polling page; guest-token exports cap it at one hour. Set `WEBDRIVER_BASEURL_USER_FRIENDLY` to your public origin or emailed links are unreachable. Downloads stream through Superset, and anyone holding the link can download until it expires, so keep the bucket private and lower the TTL if 24 hours is too long.

The export runs with the requesting user's permissions; each chart query is access-checked. Scheduled exports are not part of the feature.

## Checked

2026-11-08. Confirmed against the Exporting Dashboard Data to Excel page (read in full). Removed: the `GRANULAR_EXPORT_CONTROLS` and event-log audit advice and the generic screenshot-flag sentence (replaced by the flags named on the page); corrected that the sync row limit applies to the direct path only.
Method: documentation only; no commands were run.
