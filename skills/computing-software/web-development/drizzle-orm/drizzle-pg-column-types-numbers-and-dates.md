---
id: computing-software.web-development.drizzle-orm.drizzle-pg-column-types-numbers-and-dates
name: drizzle-pg-column-types-numbers-and-dates
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, column-types, bigint, numeric, timestamp]
level: practitioner
status: docs-checked
description: "Choose PostgreSQL column types in Drizzle: integer family, bigint modes, numeric precision, timestamp date versus string modes and timezone behavior."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/column-types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map PostgreSQL types to correct TypeScript inference.

Integers: `integer`, `smallint`, `bigint`; autoincrement types are `serial`, `smallserial`, `bigserial`. For `bigint`, for values above 2^31 but below 2^53 the docs suggest `{ mode: 'number' }` (a JS number) instead of `{ mode: 'bigint' }` (inferred as `bigint`). `bigserial` takes the same modes.

Exact decimals: `numeric({ precision: 100, scale: 20 })`, also `{ mode: 'number' }` or `{ mode: 'bigint' }`; `decimal` is an alias.

Timestamps: `timestamp({ precision: 6, withTimezone: true })`, `.defaultNow()` or `.default(sql`now()`)`. Two infer modes:
- `mode: 'date'`: Drizzle maps to a JS Date.
- `mode: 'string'`: raw strings both directions, no mapping, behavior aligned with the database.

Timezone semantics (quoted from PostgreSQL): in a literal for `timestamp without time zone`, PostgreSQL silently ignores any time zone indication; for `timestamp with time zone` the stored value is always UTC, and the docs say you get back a value converted to the timezone set in your Postgres instance. Check it with `show timezone;`.

`date({ mode: 'date' | 'string' })`, `time({ precision: 6, withTimezone: true })` and `interval({ fields: "day to second", precision: 6 })` complete the date family.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (column-types.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
