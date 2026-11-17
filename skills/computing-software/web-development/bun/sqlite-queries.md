---
id: computing-software.web-development.bun.sqlite-queries
name: sqlite-queries
category: computing-software
field: web-development
product: bun
tags: [bun-sqlite, sqlite-statements, sqlite-parameters, safe-integers]
level: practitioner
status: docs-checked
description: "Query SQLite with bun:sqlite: open modes, query versus prepare caching, all/get/run/values, named and positional parameters, strict mode, as(Class) and bigint integers."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/sqlite.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { Database } from "bun:sqlite";
const db = new Database("app.sqlite", { strict: true });   // :memory: for in-memory
const q = db.query("select $message as m;");              // cached statement
q.get({ message: "hi" });                                  // first row or null
db.query("select ?1, ?2;").all("a", "b");                  // positional
db.prepare("insert into t(x) values ($x)").run({ x: 1 }); // { lastInsertRowid, changes }
db.run("create table if not exists t(x)");                 // multi-statement strings
using db2 = new Database(":memory:");                      // closes on scope exit
```

Methods: `.all()`, `.get()`, `.run()`, `.values()`, `.raw()`, `.iterate()`, `.finalize()`.

- `db.query()` caches the 20 most recent SQL strings (SQL over 64 KB is not cached); `db.prepare()` is uncached.
- Only the first statement in a string is compiled; use `db.run()` for several.
- Parameter prefixes: `$`, `:`, `@`, `?N`. `strict: true` throws on a missing named parameter; the default binds `NULL`.
- `.as(Movie)` maps rows onto a class prototype (constructor and field initializers do not run).
- Integers are `number` by default and round beyond 53 bits; use `{ safeIntegers: true }` for `bigint`.

Gotchas: a statement has one cursor, so re-running it inside its own `for...of` makes the loop throw at its next row (use `prepare` for the inner run); `changes` excludes trigger and cascade changes.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/sqlite: constructor and strict mode, :memory:, query cache size 20 and 64 KB limit, prepare uncached, first statement only compiled, run() for several statements, parameter prefixes and positional binding, .all/.get/.run/.values/.raw/.iterate/.finalize, as(Class) skipping constructor and initializers, using, safeIntegers and 53-bit rounding, and changes excluding trigger and cascade rows. Reworded the iterate gotcha: the call works and the loop throws at its next row.
Method: documentation only; no commands were run.
