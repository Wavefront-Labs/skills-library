---
id: computing-software.database-administration.sql.dollar-quoting
name: dollar-quoting
category: computing-software
field: database-administration
product: sql
tags: [sql, dollar-quoting]
level: practitioner
status: docs-checked
description: "PostgreSQL dollar quoting for strings and function bodies without escaping quotes."
sources: ["https://www.postgresql.org/docs/current/sql-syntax-lexical.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dollar-quoted string constants

- `$$ body $$` or `$tag$ ... $tag$` is a string constant where quotes and backslashes need no escaping; nest by using different tags.
- Typical use: `CREATE FUNCTION f() RETURNS int LANGUAGE sql AS $fn$ SELECT 1 $fn$;`.
- Gotcha: a tag follows the rules of an unquoted identifier except it cannot contain a dollar sign; `$1` is a positional parameter, not a tag. A dollar-quoted string following a keyword or identifier must be separated from it by whitespace.
- Self-check: paste a body containing `'` and a backslash and confirm no escaping was needed.

## Checked

2026-11-02. Confirmed in the PostgreSQL lexical structure page: dollar-quote syntax, no escaping inside, nesting with different tags, the use for function bodies, tag rules, positional parameter `$n`, whitespace rule. Removed: the digit rule wording and the SQLite remark.
Method: documentation only; no commands were run.
