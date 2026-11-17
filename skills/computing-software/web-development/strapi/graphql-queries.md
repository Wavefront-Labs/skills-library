---
id: computing-software.web-development.strapi.graphql-queries
name: graphql-queries
category: computing-software
field: web-development
product: strapi
tags: [strapi, graphql, queries, relay, connection, pageinfo, documentid]
level: practitioner
status: docs-checked
description: "Fetch Strapi documents in GraphQL: single by documentId, flat lists, Relay-style _connection with pageInfo, and relations."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/graphql.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GraphQL queries

Single document by `documentId`:

```graphql
{
  restaurant(documentId: "a1b2c3d4e5d6f7g8h9i0jkl") {
    name
    description
  }
}
```

Flat list (plural API ID):

```graphql
restaurants {
  documentId
  title
}
```

Relay-style list: query name ends with `_connection`, returns `nodes` and `pageInfo`.

```graphql
{
  restaurants_connection {
    nodes {
      documentId
      name
    }
    pageInfo {
      pageSize
      page
      pageCount
      total
    }
  }
}
```

Relations (many-to-many `categories`) inside a flat query:

```graphql
{
  restaurants {
    documentId
    name
    categories {
      documentId
      name
    }
  }
}
```

In Relay style use `categories_connection { nodes { ... } }`.

## Limit
`pageInfo` works only at the first level; asking for `pageInfo` inside a nested `_connection` is not supported.

In mutations, relational attributes are updated by passing a `documentId` or an array of `documentId` values, depending on the relation type.

## Checked

Checked 2026-11-04 against the Strapi GraphQL API page (queries, Relay-style queries, `pageInfo` limit, mutations). Replaced the unconfirmed claim that GraphQL mutations use `connect`/`disconnect`/`set` with what the page says.

Method: documentation only; no commands were run.
