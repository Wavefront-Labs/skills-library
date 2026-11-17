---
id: computing-software.data-engineering.metabase.semantic-types
name: semantic-types
category: computing-software
field: data-engineering
product: metabase
tags: [semantic-types, data-types, field-types, foreign-key, table-metadata, casting]
level: practitioner
status: docs-checked
description: "Understand Metabase data types versus semantic types: how they drive formatting, charts and filters, why arrays and casting behave oddly, and who can edit them."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/metadata/semantic-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Data types are the column types defined in your database, such as Date or Text. Metabase reads them during sync and maps them to its own hierarchy (numeric, temporal, text, boolean, collection).

Semantic types (field types) describe a column's meaning, such as Email, Percentage, Currency, Entity key or Foreign key. The options available depend on the data type.

What they change:
- Formatting: a Percentage type shows 0.75 as 75%.
- Charts: the query builder picks chart types from data types (text gives a bar, temporal gives a line).
- Features: field filters, X-rays and URL or email extraction depend on types. Linked dashboard filters require foreign key relationships.

Gotchas:
- Arrays are not supported; array columns only offer "Is empty" and "Is not empty".
- Semantic types "should not be used for type casting". A text field tagged Quantity is still treated as text.
- Casting changes made in Table Metadata apply across the whole instance, whereas expressions like `date()` or `integer()` cast only within one query.
- Only admins and users with table metadata permissions can edit these settings.

SQL models: set the column type for each column and people can explore the model with the query builder and drill-through menus.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed the unsupported claim that query-builder joins rely on foreign key types (the page names only dashboard linked filters) and added the SQL model point. Otherwise unchanged.
