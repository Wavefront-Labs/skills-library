---
id: computing-software.web-development.appwrite.appwrite-csv-import-export
name: appwrite-csv-import-export
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, csv, import, export, migration]
level: practitioner
status: docs-checked
description: "Import rows from CSV into a matching table and export filtered columns to CSV with custom delimiters and headers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/csv-imports/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/csv-exports/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move tabular data in and out.

Import (Cloud and self-hosted; runs as a background task with a floating progress bar; Console: Databases > table > Import CSV, uploading a file or choosing one from a Storage bucket):
1. Create the table and its columns first; the CSV must match and include all required columns.
2. Headers map to column keys. Optional `$id` sets row IDs; optional `$createdAt` and `$updatedAt` must be ISO 8601 strings like `2025-08-10T12:34:56.000Z`.
3. Rows are validated and imported in batches of 100. If a supplied ID already exists, the whole batch containing it fails while other batches continue.
4. Empty values: text columns become empty strings (write `null` unquoted for real null), integer and boolean columns become null, arrays become empty arrays.
5. Array columns take a quoted comma list such as `"one,two"`.

Export (Cloud and self-hosted; Console: Databases > table > Export CSV; large exports run in the background and you get an email with a short-lived download link):
- Apply table filters in the Console so only matching rows export, and select the columns you want. System columns `$id`, `$createdAt` and `$updatedAt` are always included.
- Choose a delimiter (comma, tab, semicolon or pipe) and whether to include a header row.
- Relationships export as related row IDs only. `$createdAt` and `$updatedAt` export in ISO 8601. If row-level security is on, a `$permissions` column is included, and on import a `$permissions` column such as `"read(""any""),update(""users"")"` sets row permissions.

Gotcha: a duplicate ID loses its entire 100-row batch, so de-duplicate before importing.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages CSV imports and CSV exports: Cloud and self-hosted availability, matching columns and required columns, `$id`, `$createdAt`/`$updatedAt` as ISO 8601 with the example value, batches of 100 and whole-batch failure on a duplicate ID, empty-value rules per type, quoted comma lists for arrays, filters, column selection, always-included system columns, delimiters, header row, relationship IDs, background processing. Added the Console button names, `$permissions` and email-link behaviour from the same pages. Removed: the Verify step, which is practical advice rather than a documented claim.
Method: documentation only; no commands were run.
