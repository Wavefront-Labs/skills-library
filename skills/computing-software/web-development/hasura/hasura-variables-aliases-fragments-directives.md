---
id: computing-software.web-development.hasura.hasura-variables-aliases-fragments-directives
name: hasura-variables-aliases-fragments-directives
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, variables, aliases, fragments, directives, graphql]
level: intro
status: docs-checked
description: "Make Hasura queries reusable with variables, aliases for repeated fields with different args, fragments and include or skip directives."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/variables-aliases-fragments-directives.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write maintainable GraphQL operations.

Variables make a query re-usable:
```graphql
query getArticles($author_id: Int!, $title: String!) {
  articles(where: { author_id: { _eq: $author_id }, title: { _ilike: $title } }) { id title }
}
```
Send `{"author_id": 1, "title": "%How to%"}` as variables.

Aliases return objects under a different name than the field, which is useful for fetching the same type with different arguments in one query:

```graphql
query {
  topTwoArticles: articles(order_by: {rating: desc}, limit: 2) { title rating }
  worstArticle: articles(order_by: {rating: asc}, limit: 1) { title rating }
}
```
Fragments name a reusable set of fields:

```graphql
fragment articleFields on articles { id title }
query { articles { ...articleFields } }
```
Directives include or skip a field based on a boolean query variable:

```graphql
query getArticles($with_publisher: Boolean!) {
  articles { title publisher @include(if: $with_publisher) }
}
```
With `@include(if: Boolean)` the field is in the result when the value is true; with `@skip(if: Boolean)` it is left out when the value is true.

## Checked
2026-11-07. Read in full the single cited page (variables-aliases-fragments-directives.mdx, GitHub file view; no snippet files, only inline GraphiQL components).
Confirmed: the variables example and values, aliases wording and example, fragment example, @include and @skip semantics.
Removed: the claim that caching treats variable values as part of the cache key (not on this page), and the invented Verify step.
Method: documentation only; no commands were run.
