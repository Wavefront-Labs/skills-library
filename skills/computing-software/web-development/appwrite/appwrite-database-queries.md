---
id: computing-software.web-development.appwrite.appwrite-database-queries
name: appwrite-database-queries
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, queries, filtering, tablesdb]
level: practitioner
status: docs-checked
description: "Filter rows with the Query class, including select, comparison, text, null, logical, time and geo operators."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/queries/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build correct `queries` arrays.

Basics: pass `queries: [...]` built with the SDK `Query` class to `listRows` and similar endpoints. Separate query methods are combined with AND. For OR across values, pass several values in one method: `Query.equal('title', ['Avatar', 'Lord of the Rings'])`. The default page size is 25.

Operator families listed in the docs:
- `Query.select(['name', 'age'])` picks columns. Relationship columns hold only row IDs by default; select them explicitly, for example `Query.select(['*', 'reviews.*'])` or nested `['*', 'reviews.*', 'reviews.author.*']`.
- Comparison: equal, notEqual, lessThan, lessThanEqual, greaterThan, greaterThanEqual, between (inclusive bounds) and notBetween (bounds excluded).
- Null checks: isNull, isNotNull.
- Text: startsWith, endsWith, contains (arrays and text) and their `not` forms, plus search and notSearch (search strings must be at least 3 characters).
- Logical: `Query.and([...])` and `Query.or([...])` take arrays of nested queries.
- Ordering and pagination: orderDesc and orderAsc (the column must be indexed), orderRandom, limit, offset, cursorAfter, cursorBefore.
- Time helpers (ISO 8601 date-time strings): createdBefore, createdAfter, updatedBefore, updatedAfter.
- Geo (on spatial columns, coordinates as `[longitude, latitude]`): distanceEqual, distanceNotEqual, distanceGreaterThan, distanceLessThan, intersects, overlaps, touches, crosses and their `not` forms; equal, notEqual, contains and notContains also work on spatial columns.

REST and GraphQL receive each query as a JSON string, for example `{"method":"equal","column":"title","values":["Avatar","Lord of the Rings"]}`.

Gotcha: search needs a full-text index on the queried columns. The hyphen is a stop character in search, so wrap exact values with hyphens in quotes inside the search string, for example `Query.search(column, '"SWT-2621-44"')`.

Combine groups with nesting, for example `Query.or([Query.and([...]), Query.and([...])])`.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Queries (databases/queries), read from the raw markdown because the rendered page was truncated: the `queries` parameter, AND between separate methods, OR via multiple values, the default of 25 items, every operator named, the select patterns, the 3-character search rule, the indexed-column ordering rule, the ISO 8601 time helpers, spatial operators and the JSON form. Removed: the Console-versus-SDK count Verify step.
Method: documentation only; no commands were run.
