---
id: computing-software.database-administration.neo4j.string-and-list-functions
name: string-and-list-functions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, substring, split-function, reduce-function, scalar-functions, string-functions, aggregating-functions, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Common functions"
sources:
  - https://neo4j.com/docs/cypher-manual/current/functions/string/
  - https://neo4j.com/docs/cypher-manual/current/functions/list/
  - https://neo4j.com/docs/cypher-manual/current/functions/scalar/
  - https://neo4j.com/docs/cypher-manual/current/expressions/predicates/string-operators/
  - https://neo4j.com/docs/cypher-manual/current/values-and-types/working-with-null/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String and list functions

Goal: use built-ins instead of client code.
- Documented: `toLower`, `trim`, `split`, `substring`, `replace`, `toInteger`, `coalesce`, `range`, `reduce`, `size`.
- To test for null use `v IS NULL` or `v IS NOT NULL`.
- `=~` matches with regular expressions using Java regex syntax; flags such as `(?i)` go at the start of the expression.
Verify: edge cases with null and empty strings return expected values.

## Checked

2026-11-02. Confirmed: function names, `IS NULL` advice, `=~` and Java regex flags (string, list, scalar, string-operators, working-with-null). Removed: the full-match wording and 'comparisons with null yield null' sentence (not found in the pages read).
Method: documentation only; no commands were run.
