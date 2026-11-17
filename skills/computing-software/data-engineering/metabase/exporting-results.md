---
id: computing-software.data-engineering.metabase.exporting-results
name: exporting-results
category: computing-software
field: data-engineering
product: metabase
tags: [export, download-row-limit, csv, xlsx, pivot-export, pdf]
level: intro
status: docs-checked
description: "Export Metabase results: formats, formatted versus raw values, the 1,048,575 row default and MB_DOWNLOAD_ROW_LIMIT, Excel cell limits, and dashboard PDF export."
sources:
  - https://www.metabase.com/docs/latest/questions/exporting-results
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Question exports: `.csv`, `.xlsx`, `.json`, and `.png` (charts only) from the Download button at the lower right of a question.

Formatting: formatted exports keep your Metabase formatting; unformatted exports contain raw values, so extra decimal places can appear. Pivot tables export pivoted by default, or unpivoted if you choose; the pivoted output is a flat table, not a native Excel PivotTable.

Limits:
- Default row limit is the first 1,048,575 rows.
- CSV limits can be raised with `MB_DOWNLOAD_ROW_LIMIT`, which may hurt performance.
- XLSX is always capped at Excel's maximum row count.
- Excel cells are capped at 32,767 characters; longer content is truncated.

Dashboards: export as PDF from Share; on multi-tab dashboards use "Export tab as PDF". The PDF shows charts as currently visible. For a card, use the three-dot menu and Download results; holding Option (Mac) or Alt (Windows) exports raw, unformatted data. Scheduled PDFs and attachments come from dashboard subscriptions.

Gotchas:
- If the export option is missing, check download permissions.
- Exports carry Metabase branding unless you have a Pro or Enterprise plan.
- Public links and alerts can also deliver exports.

## Checked
2026-11-03. Confirmed against the Metabase docs page Questions, Exporting results: formats, formatted versus unformatted, pivot export behaviour, 1048575 default row limit and MB_DOWNLOAD_ROW_LIMIT for CSV, XLSX cap, 32,767 cell characters, dashboard PDF and tab PDF, card download and Option/Alt raw export, subscriptions, branding on non-Pro plans. Nothing removed.
Method: documentation only; no commands were run.
