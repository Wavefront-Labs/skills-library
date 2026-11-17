---
id: computing-software.web-development.appwrite.appwrite-rows-crud-list-caching
name: appwrite-rows-crud-list-caching
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, rows, crud, caching, tablesdb]
level: practitioner
status: docs-checked
description: "Create and list rows with TablesDB, skip expensive totals, and cache list responses with a ttl."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/rows/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: day-to-day row operations.

Create: `tablesDB.createRow({ databaseId, tableId, rowId: ID.unique(), data: {...} })`. Users need create permission at the table level to create rows.

List: `tablesDB.listRows({ databaseId, tableId, queries: [Query.equal('title', 'Avatar')] })`. Read permission at table level is required. Results are limited to 25 rows by default; use pagination to change that.

Skip totals: pass `total: false` on list calls when your UI does not need an exact count (infinite scroll, load more). The response shape is unchanged but `total` is `0`, which reduces latency on large or filtered tables.

Cache list responses: pass `ttl` in seconds to `listRows`, from 1 to 86400 (24 hours); default is 0 (disabled). The cache is permission-aware, so users with different roles never see each other's cached data. The response header `X-Appwrite-Cache` is `hit` or `miss`.

GraphQL exists too (`tablesCreateRow`, `tablesListRows`). In the Console you can add rows by opening the table's Rows tab and clicking Add row.

Gotcha: row writes do not invalidate the list cache, but schema changes do. To purge it, call `updateTable` with `purge: true` from a Server SDK.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/databases/rows. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify; Gotcha replaced by the page statement that row writes do not invalidate the cache while schema changes do, and purging via updateTable with purge: true from a Server SDK.

Method: documentation only; no commands were run.
