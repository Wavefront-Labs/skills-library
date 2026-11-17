---
id: computing-software.web-development.drizzle-orm.drizzle-eslint-plugin-where-rules
name: drizzle-eslint-plugin-where-rules
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, eslint, enforce-delete-with-where, enforce-update-with-where, lint]
level: intro
status: docs-checked
description: "Install eslint-plugin-drizzle and enforce .where() on delete and update, with drizzleObjectName to limit rules to Drizzle clients."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/eslint-plugin.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop accidental whole-table deletes and updates in code review.

Install `eslint-plugin-drizzle` plus `@typescript-eslint/eslint-plugin` and `@typescript-eslint/parser`. Example `.eslintrc.yml`:

```yml
root: true
parser: '@typescript-eslint/parser'
parserOptions:
  project: './tsconfig.json'
plugins:
  - drizzle
rules:
  'drizzle/enforce-delete-with-where': "error"
  'drizzle/enforce-update-with-where': "error"
```

Or extend `plugin:drizzle/all` or `plugin:drizzle/recommended`; at the time of the docs these two are equivalent.

Rules:
- `enforce-delete-with-where`: a `.delete()` statement must have `.where()`.
- `enforce-update-with-where`: an `.update()` statement must have `.where()`.

Both match any object with a `delete` or `update` method, so unrelated classes get flagged too. Restrict with `drizzleObjectName` (string or string array):

```yml
rules:
  'drizzle/enforce-delete-with-where':
    - "error"
    - "drizzleObjectName":
      - "db"
```

With that setting `db.delete()` is flagged but `myClassObj.delete()` is not. The same `drizzleObjectName` option exists on `enforce-update-with-where`. The plugin exists for cases where a type check cannot cover a scenario or its error would be hard to understand; the docs say most of the time you do not need to delete or update all rows in a table.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (eslint-plugin.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
