---
id: computing-software.web-development.hasura.hasura-insert-mutations
name: hasura-insert-mutations
category: computing-software
field: web-development
product: hasura
tags: [hasura, mutations, insert, nested-insert, postgres]
level: practitioner
status: docs-checked
description: "Insert one or many rows with Hasura insert_<table> and insert_<table>_one mutations, including nested inserts through relationships."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/mutations/postgres/insert.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write correct insert mutations.

Generated schema for table `article`:
- `insert_article(objects: [article_insert_input!]!, on_conflict: article_on_conflict)` returning `article_mutation_response` with `affected_rows` and `returning`; `objects` is required and takes several objects.
- `insert_article_one(object: article_insert_input!, on_conflict: ...)` returning the row directly (from v1.2.0; only available with select permission on the table).

Tables outside the `public` schema use `insert_<schema>_<table>`.

Examples:
```graphql
mutation {
  insert_article_one(object: { title: "Hello", author_id: 1 }) { id title }
}
```
Nested insert through relationships (object or array) using the `data` key:

```graphql
mutation {
  insert_authors(objects: [{
    name: "John",
    address: { data: { location: "San Francisco" } },
    articles: { data: [ { title: "GraphQL Guide", content: "..." } ] }
  }]) { affected_rows returning { id address { id } } }
}
```
Variables work with the input types, for example `$object: article_insert_input!` or `$objects: [article_insert_input!]!`.

Add `on_conflict` to turn an insert into an upsert (see the upsert skill).

How nested inserts run: object-relationship rows are inserted first, then the parent (its foreign key is set from that row), then array-relationship rows last. So you cannot pass the foreign key (`address_id`, or `author_id` in the child data) yourself when also supplying that relationship's data. `insertion_order` on a manual relationship controls the order, which one-to-one nested inserts may need to avoid a `Not-NULL violation`.

Other rules: for many-to-many, insert through the bridge table with nested `data` and an `on_conflict` on the related table. Omit a field to use its default value, whether from Postgres defaults or column presets. Array-typed columns take a Postgres array literal such as `"{a, b}"`.

Gotcha: without select permission on the table, `insert_<table>_one` is not available.

## Checked

2026-11-04. Confirmed against the cited pages: insert page: generated schema, naming for non-public schemas, single and multiple inserts, nested insert ordering and FK restrictions, insertion_order, many-to-many, defaults, array literals. Removed or corrected: the claim that presets and checks apply to nested inserts, the insert-permission requirement wording and the Verify step.

Method: documentation only; no commands were run.
