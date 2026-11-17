---
id: computing-software.web-development.drizzle-orm.drizzle-seed-generators-reference
name: drizzle-seed-generators-reference
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-seed, seed, generators, refine]
level: advanced
status: docs-checked
description: "Use drizzle-seed generators through seed(db, schema, { count }).refine(): default, valuesFromArray, intPrimaryKey and number with their options."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/seed-functions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the data drizzle-seed generates per column.

Pattern:

```ts
import { seed } from "drizzle-seed";
await seed(db, schema, { count: 1000 }).refine((funcs) => ({
  posts: { columns: { content: funcs.default({ defaultValue: "post content" }) } },
}));
```

`refine` receives `funcs` and returns per-table config with `columns`. Generators covered here:

- `default({ defaultValue, arraySize? })`: generates the same given value each time.
- `valuesFromArray({ values, isUnique?, arraySize? })`: values taken from an array, which can be weighted as `{ weight: number; values: any[] }[]`; `isUnique` defaults to the database column's uniqueness.
- `intPrimaryKey()`: sequential integers starting from 1; no parameters.
- `number({ isUnique?, precision?, maxValue?, minValue?, arraySize? })`: floating-point numbers in a range; `precision` defaults to 100 (10 means accurate to one tenth, 100 to one hundredth), `maxValue` defaults to `precision * 1000` if not unique or `precision * count` if unique, `minValue` defaults to `-maxValue`.

`arraySize` is the number of elements in each one-dimensional array; if specified, arrays are generated. The page's warning: specifying `arraySize` along with `isUnique` generates unique values which are then packed into arrays, not unique arrays.

The page documents more generators with the same call shape, for example `int`, `boolean`, `date`, `time`, `timestamp`, `datetime`, `year`, `json`, `interval`, `string`, `uuid`, `firstName`, `lastName`, `fullName`, `email` and `phoneNumber`; check the page for their parameters and defaults.

## Checked

Date: 2026-11-07

Confirmed against `seed-functions.mdx` in the drizzle-orm-docs repo (cloned from main). The page is 1328 lines; lines 1 to 700 were read (the warning, then every generator from `default` through the start of `phoneNumber`), and the remaining lines were not read. Everything stated above comes from the read part: the four generators' parameter tables, defaults, examples and the arraySize warning.

Removed: the invented Verify step. Listed the other generator names (seen as headings in the read part) without their parameters.

Method: documentation only; no commands were run.
