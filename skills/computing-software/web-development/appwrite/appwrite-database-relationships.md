---
id: computing-software.web-development.appwrite.appwrite-database-relationships
name: appwrite-database-relationships
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, relationships, tablesdb, performance]
level: advanced
status: docs-checked
description: "Model related tables with relationship columns and load related rows only when you select them."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/relationships/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/queries/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid duplicated data and fetch related rows deliberately.

Concept: a relationship column stores the ID of related rows and is null when there are none. Storing users and posts in separate tables avoids update anomalies (changing a user name in hundreds of copied rows).

Directionality: one-way (visible from one side, like a tree) or two-way (visible from both sides, like a graph). Types: one-to-one, one-to-many, many-to-one, many-to-many. On-delete behaviour: Restrict (a row with related rows cannot be deleted), Cascade (related rows are deleted too), Set null (related rows are kept with the relationship column set to null).

Opt-in loading: by default rows return only their own fields; related rows are not loaded. Request them with `Query.select`: choose specific columns, load relationship data, load specific fields from both main and related rows, or nest relationships. This keeps payloads small and performance predictable.

Example idea: `queries: [Query.select(['name', 'age'])]` returns just those fields; selecting the relationship column (with sub-fields) returns the related row data.

Limits from other pages: bulk operations are not supported on tables that contain relationship columns, and CSV export includes only related row IDs by default.

Gotcha: if the on-delete behaviour is set null, deleting a row leaves related rows in place; to delete them as well they must be deleted individually. A row that can relate to only one row can drop the relationship by setting the relationship column to `null`.

Related-row loading is explicit: "relationship columns contain only row IDs" unless you include relationship fields, such as `['*', 'reviews.*']`, in `Query.select`.


## Checked

2026-11-04. Confirmed against the Appwrite docs pages Relationships (databases/relationships) and Queries: relationship columns holding related IDs and null when empty, update anomalies, opt-in loading, one-way and two-way, the four types, the three on-delete behaviours, deleting and nulling, and the select patterns. The bulk and CSV limits are confirmed on the Bulk operations and CSV exports pages. Removed: the claim about a regression "after an upgrade" to opt-in loading, and the response-shape Verify step.
Method: documentation only; no commands were run.
