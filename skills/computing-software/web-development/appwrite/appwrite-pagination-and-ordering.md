---
id: computing-software.web-development.appwrite.appwrite-pagination-and-ordering
name: appwrite-pagination-and-ordering
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, pagination, ordering, cursor, offset]
level: practitioner
status: docs-checked
description: "Page through rows with limit and offset or cursors, choose between them, and order by columns or the automatic $sequence field."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/pagination/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/order/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reliable lists at any size.

Defaults: 25 rows per page; change with `Query.limit(n)`. No hard maximum, but large pages hurt performance.

Offset pagination: `Query.limit(25)` plus `Query.offset(25)`. It supports page-number UIs but slows as offsets grow and can produce missing or duplicate rows when data changes. Use for rarely changing tables (a countries list, up to about 20 pages).

Cursor pagination: after reading a page pass the last row ID to `Query.cursorAfter(lastId)`; use `Query.cursorBefore(firstId)` to go back. Best for frequently updated tables, feeds, chat and infinite scroll.

Skip totals: `total: false` avoids the extra COUNT on large tables; `total` then returns 0.

Ordering: `Query.orderAsc('title')` and `Query.orderDesc('year')`; add several for multi-column sorting (title ascending, then year descending). For performance create an index on the first ordered column. Appwrite adds a numeric `$sequence` to every row that increments per insert, handy for stable insertion-order paging: `Query.orderAsc('$sequence')`.

Gotcha: offset pagination on frequently updated tables can return missing and duplicate results; use cursors there.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/databases/pagination, products/databases/order. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify step; Gotcha reworded to the page (offset on frequently updated tables gives missing and duplicate results).

Method: documentation only; no commands were run.
