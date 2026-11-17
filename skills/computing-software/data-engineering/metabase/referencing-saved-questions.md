---
id: computing-software.data-engineering.metabase.referencing-saved-questions
name: referencing-saved-questions
category: computing-software
field: data-engineering
product: metabase
tags: [saved-questions, model-reference, cte, hash-syntax, native-query]
level: practitioner
status: docs-checked
description: "Reference saved questions and models inside Metabase SQL with the {{#id-name}} syntax, use them in CTEs, and respect the same-database and no-variables limits."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/referencing-saved-questions-in-queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: type `{{#search term}}` to get a typeahead of models and questions, or write `{{#ID-name}}`. Only the `#` and the ID are required; Metabase shows the name for readability. Find the ID in the URL after `/model/` or `/question/`.

In a CTE:

```sql
WITH gizmo_orders AS {{#5-gizmo-orders-in-2019}}
```

At run time Metabase substitutes the referenced SQL, wrapped in parentheses.

Limitations:
- Works only with SQL databases that support the feature, such as PostgreSQL, MySQL, Snowflake and SQL Server. CTEs need a database that supports them.
- The model or question must use the same database selected in the native editor.
- Variables inside the referenced query are not accessible; you get only its results.
- If a saved question uses a field filter, you cannot change that filter from your query. Update or duplicate the question and apply the filter there.

Gotcha: if expected items are missing from the typeahead, check the selected database, because search only shows items for that database.

The page's motivating example: run a complicated query once, save it as a model, and let people refer to it like any other table.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Claims matched the page; only the closing line was replaced with the page's own example. Otherwise unchanged.
