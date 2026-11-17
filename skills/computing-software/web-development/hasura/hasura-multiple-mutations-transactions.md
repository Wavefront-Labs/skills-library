---
id: computing-software.web-development.hasura.hasura-multiple-mutations-transactions
name: hasura-multiple-mutations-transactions
category: computing-software
field: web-development
product: hasura
tags: [hasura, mutations, transactions, rollback, remote-schema, actions]
level: practitioner
status: docs-checked
description: "Run several Hasura mutations in one request that execute sequentially in a single transaction and roll back together, with the Actions and remote schema exception."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/mutations/postgres/multiple-mutations.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: atomic multi-step writes.

Behaviour from the docs: if multiple mutations are in the same request they execute sequentially in a single transaction; if any fails, all executed mutations roll back.

Example (from the docs, values changed): delete an author's articles and update the author in one request:

```graphql
mutation reset_author {
  delete_article(where: { author_id: { _eq: 6 } }) { affected_rows }
  update_author(where: { id: { _eq: 6 } }, _set: { name: "Cory" }) {
    returning { id name }
  }
}
```
Related pattern: use nested inserts (an object and its related objects in one mutation) to insert linked rows together, for example an article with its author:
`insert_article(objects: [{ title: "Article 1", content: "...", author: { data: { name: "Cory" } } }])`.

Gotcha: in requests where a Remote Schema or an Action is present and a mutation fails, rollback is not possible; mutations executed before the failed one still succeed.

## Checked
2026-11-07. Read in full the single cited page (multiple-mutations.mdx, GitHub file view; no snippet files, only inline GraphiQL components).
Confirmed: sequential execution in a single transaction, rollback of all executed mutations, the Remote Schema/Action exception, the delete plus update example, the nested insert of an article with its author.
Removed: the alias advice (not on the page), the "keep database-only mutations in their own request" advice (not on the page), the invented Verify step, and `affected_rows` on the update (the page returns `returning`).
Method: documentation only; no commands were run.
