---
id: computing-software.web-development.hasura.hasura-table-relationships-foreign-keys
name: hasura-table-relationships-foreign-keys
category: computing-software
field: web-development
product: hasura
tags: [hasura, relationships, foreign-key, postgres, metadata, nested-queries]
level: practitioner
status: docs-checked
description: "Create object and array relationships in Hasura from a foreign key so nested queries work, via the Console, tables.yaml, or Metadata API."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/table-relationships/create.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect tables so GraphQL can nest related objects.

Steps:
1. Add a foreign key (migration up.sql):

```sql
ALTER TABLE articles ADD FOREIGN KEY (author_id) REFERENCES authors(id);
```
with a matching down.sql that drops constraint `articles_author_id_fkey`.
2. Create the relationships. The Console infers candidates from the foreign key and recommends them in the Relationships tab. In metadata (tables.yaml):

```yaml
- table: {schema: public, name: articles}
  object_relationships:
    - name: author
      using:
        foreign_key_constraint_on: author_id
- table: {schema: public, name: authors}
  array_relationships:
    - name: articles
      using:
        foreign_key_constraint_on:
          column: author_id
          table: {schema: public, name: articles}
```
3. Run `hasura migrate apply` then `hasura metadata apply`. The Metadata API equivalents are `pg_create_object_relationship` and `pg_create_array_relationship`.

Notes:
- A relationship involving a view or Native Query cannot use a foreign key (they cannot carry one), so it is defined manually; the page shows `manual_configuration` with `column_mapping` (and `remote_table` for a view, `remote_native_query` for a Native Query).
- Each article has one author: an object relationship. An author has many articles: an array relationship.
- The Console can also track relationships inferred from existing foreign keys from the Data -> Schema page (individually or with Track all).

## Checked
2026-11-07. Read in full the single cited page (create.mdx, GitHub file view; no snippet files, only inline GraphiQL, Tabs and Thumbnail components).
Confirmed: up.sql/down.sql statements and constraint name, Console inference, the tables.yaml shapes, `hasura migrate apply` / `hasura metadata apply`, both Metadata API type names, manual relationships for views and Native Queries, object vs array wording.
Removed: the "object relationships do not expose the where argument" gotcha (not on the page) and the invented Verify step.
Method: documentation only; no commands were run.
