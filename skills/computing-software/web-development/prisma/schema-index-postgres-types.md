---
id: computing-software.web-development.prisma.schema-index-postgres-types
name: schema-index-postgres-types
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-index-types-postgres, prisma, gin-index, hash-index, brin-operator-class, raw-ops]
level: advanced
status: docs-checked
description: "Create PostgreSQL Hash, Gin, Gist, SpGist and Brin indexes with @@index type and ops, and handle operator classes, CockroachDB limits and function indexes."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/indexes.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PostgreSQL index types

`@@index([field], type: X)` (PostgreSQL only; `BTree` is the default). Supported: `Hash`, `Gist`, `Gin`, `SpGist`, `Brin`.

- Hash: `@@index([value], type: Hash)` gives `CREATE INDEX ... USING HASH`. Only `=` and `<>` use it; `<` and `>` become much slower than with BTree.
- Gin: for composite values such as arrays and JSONB. `@@index([value(ops: JsonbPathOps)], type: Gin)` on a `Json` field creates `USING GIN (value jsonb_path_ops)` and speeds `@>` queries. Operator classes: `ArrayOps` (any array, default), `JsonbOps` (default for `@db.JsonB`), `JsonbPathOps`.
- Gist: `value String @db.Inet` with `@@index([value(ops: InetOps)], type: Gist)` supports IP comparisons like `value > '10.0.0.2'`. `InetOps` is the supported class.
- SpGist: `@@index([value], type: SpGist)`; default ops `TextOps` (for `String`, `@db.Text` and `@db.VarChar`) and `InetOps` (PostgreSQL 10+). Helps `LIKE 'something%'`.
- Brin: for large, insert-once data such as timestamps, for example `@@index([value(ops: Int4BloomOps)], type: Brin)`. The docs list `*MinMaxOps` (mostly the defaults), `*BloomOps` and `*MinMaxMultiOps` classes per native type; Bloom and MinMaxMulti need PostgreSQL 14 or later. Default class may be omitted.

Operator classes from PostgreSQL 10 and later are generally supported. If the class needs an unsupported field type, pass a string with `raw("other")` to skip validation.

CockroachDB: only GIN and BTree exist, and `ops` is neither needed nor allowed.

Warning: indexes on a function result (such as `to_tsvector`) are not supported and do not show up in `prisma db pull`.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/indexes pages, orm/v7): type argument and the Hash, Gist, Gin, SpGist, Brin methods, generated SQL, operator-class tables (JsonbPathOps, InetOps, TextOps, Int4BloomOps), PostgreSQL 10+/14+ gates, raw("other"), CockroachDB GIN/BTree-only and no ops, function-index warning. Reworded the MinMaxOps default claim.

Method: documentation only; no commands were run.
