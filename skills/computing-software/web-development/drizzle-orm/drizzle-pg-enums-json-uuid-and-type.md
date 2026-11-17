---
id: computing-software.web-development.drizzle-orm.drizzle-pg-enums-json-uuid-and-type
name: drizzle-pg-enums-json-uuid-and-type
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, pgenum, jsonb, uuid, type-override]
level: practitioner
status: docs-checked
description: "Declare pgEnum, json/jsonb with $type, uuid defaultRandom and branded types via $type() in Drizzle PostgreSQL schemas."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/column-types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: model enums, JSON and ids with accurate types.

Enums:

```ts
export const moodEnum = pgEnum('mood', ['sad', 'ok', 'happy']);
export const table = pgTable('table', { mood: moodEnum() });
```

The docs show this producing `CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');` and a column of type `"mood"`.

JSON: `json()` and `jsonb()` accept `.default({ foo: 'bar' })` or `.default(sql`'{"foo": "bar"}'`)`. Use `.$type<{ foo: string }>()` for object inference; it will not check runtime values but provides compile-time protection for default values, insert and select schemas (for example `.$type<string[]>().default({})` won't compile).

UUID: `uuid().defaultRandom()` generates `gen_random_uuid()` in the database; a literal default may be passed with `.default('...')`.

Any column builder has `.$type<T>()` for custom or branded types:

```ts
type UserId = number & { __brand: 'user_id' };
id: serial().$type<UserId>().primaryKey(),
```

Other types documented: `boolean`, `text`, `varchar`, `char`, `real`, `double precision`, `bytea`, `point`, `line`, `inet`, `cidr`, `macaddr`, `macaddr8`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (column-types.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
