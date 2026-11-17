---
id: computing-software.data-engineering.metabase.sql-snippets
name: sql-snippets
category: computing-software
field: data-engineering
product: metabase
tags: [sql-snippets, snippet-syntax, reusable-sql, archive, native-editor]
level: practitioner
status: docs-checked
description: "Create and reference Metabase SQL snippets with the exact whitespace-sensitive syntax, nesting rules, parameter handling, permissions and what breaks when you rename them."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/snippets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reference a snippet as `{{snippet: name}}`. Metabase is whitespace sensitive: no space between `{{` and `snippet`, but a space after the colon.

Create: highlight SQL in the native editor, right-click and choose "Save as snippet", or create one from the Snippets sidebar. Names must be unique, even against archived snippets.

Nesting: snippets can reference other snippets, but circular references are disallowed. They can also contain SQL parameters, table variables and saved question references.

Parameters: settings belong to the question, not the snippet. Same-named parameters across snippets in one question show as a single parameter.

Permissions: users with native editor access to at least one database can create, edit and archive all snippets, including those tied to databases they cannot query. Some plans add snippet folders with their own permissions.

Gotchas:
- Broken code in a snippet breaks every question that uses it.
- Renaming a snippet breaks other snippets that reference it.
- Outer queries must use any aliases defined inside a snippet.
- Snippets cannot be deleted, only archived; archiving does not affect existing queries.
- The eye icon previews the full query with snippets substituted.

Snippets can define standardized KPIs and filters in SQL, much as metrics and segments do in the query builder (for example, exactly how revenue is calculated). Editing a snippet's code updates every question that uses it.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Claims matched the page; only the closing line was reworded to what the page states. Otherwise unchanged.
