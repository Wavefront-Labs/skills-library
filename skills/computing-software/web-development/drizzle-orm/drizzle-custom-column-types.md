---
id: computing-software.web-development.drizzle-orm.drizzle-custom-column-types
name: drizzle-custom-column-types
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, customtype, custom-types, todriver, fromdriver]
level: advanced
status: docs-checked
description: "Define custom column types with customType: dataType, toDriver/fromDriver transforms, config generics, defaults and the newer codec option."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/custom-types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a column type Drizzle does not ship.

```ts
import { customType, pgTable } from 'drizzle-orm/pg-core';
const customText = customType<{ data: string }>({
  dataType() { return 'text'; },
});
export const users = pgTable('users', { name: customText().notNull() });
```

With config and transformation (the docs rebuild `timestamp` this way):

```ts
const customTimestamp = customType<{
  data: Date; driverData: string;
  config: { withTimezone: boolean; precision?: number }; configRequired: false;
}>({
  dataType(config) {
    const precision = typeof config?.precision !== 'undefined' ? ` (${config.precision})` : '';
    return `timestamp${precision}${config?.withTimezone ? ' with time zone' : ''}`;
  },
  fromDriver(value: string): Date { return new Date(value); },
});
// used as customTimestamp('created_at', { withTimezone: true })
```

Generic keys: `data` (required, the TS type), `driverData`, `config`, `configRequired` (default false), `notNull`, `default`. `driverOutput` and `jsonData` are deprecated in favor of codecs.

Methods: `dataType` (required SQL type string, may use `config`), `toDriver` (TS to driver), `fromDriver` (driver to TS), `codec` (named driver codec, see the Codecs page), and deprecated `fromJson` and `forJsonSelect`.

Two transform layers run in order: writes apply `toDriver` first, then the codec; reads apply the codec first, then `fromDriver`. If neither is set, values pass through untouched. Often a codec variant removes the need for `fromDriver`: the docs show `codec: 'bigint:number'` returning a number directly where `codec: 'bigint'` plus `fromDriver` would otherwise be needed.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (custom-types.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
