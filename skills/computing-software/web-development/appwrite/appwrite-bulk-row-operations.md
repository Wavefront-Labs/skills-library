---
id: computing-software.web-development.appwrite.appwrite-bulk-row-operations
name: appwrite-bulk-row-operations
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, bulk, server-sdk, tablesdb]
level: advanced
status: docs-checked
description: "Create, update, upsert or delete many rows in one server-side request with atomic all-or-nothing behavior and plan limits."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/bulk-operations/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut API calls on large data sets.

Methods: `createRows`, `updateRows`, `upsertRows` and `deleteRows` on `TablesDB`. They are available only through the server-side SDKs. Client SDKs do not support bulk operations by design, to prevent abuse and protect against unexpected costs; for client apps that need bulk-like behaviour, use an Appwrite Function with rate limiting and validation.

Atomic: bulk operations are all-or-nothing. If you create 100 rows and one fails validation, none of the 100 is created.

Plan limits (rows per request, all bulk operations): Free 100, Pro 1,000. For more than Pro allows, inquire about a custom plan.

Events: bulk operations trigger Functions, Webhooks or Realtime events for each row manipulated, not one event for the whole request. Large batches therefore fan out into many events.

Restrictions: tables that contain relationship columns are not supported in bulk operations; use individual row operations.

Permissions: update needs update permission at the table level; upsert needs create and update; delete needs delete permission.

Timestamps: when creating, updating or upserting in bulk you can set `$createdAt` and `$updatedAt` per row in the payload as ISO 8601 date-time strings. If omitted, Appwrite sets them.

Deleting: `deleteRows` takes queries to select rows; with no queries, all rows in the table are deleted.

Transactions: all bulk operations accept `transactionId`; Appwrite then stages the request and applies it on commit.

## Checked

2026-11-04. Confirmed against the Appwrite docs page Bulk operations (databases/bulk-operations): method names, server-SDK-only rule and its reason, atomic behaviour and the 100-row example, Free 100 and Pro 1,000 rows per request, per-row events, relationship-table restriction, required permissions, custom timestamps (ISO 8601), delete-without-queries behaviour, and `transactionId`. Removed: the Verify step and the "with an API key" condition on timestamps, which that page does not state.
Method: documentation only; no commands were run.
