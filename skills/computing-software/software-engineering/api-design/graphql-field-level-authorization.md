---
id: computing-software.software-engineering.api-design.graphql-field-level-authorization
name: graphql-field-level-authorization
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-authorization, field-level-authorization, api-security]
level: advanced
status: docs-checked
description: "Authorize GraphQL at the type and field level by delegating the decision to the business logic layer, with resolvers calling it and optional schema directives."
sources:
  - https://graphql.org/learn/authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL field-level authorization

**Goal:** make sure every field a client selects is checked against who is asking, with one source of truth.

## Rules from the GraphQL guide
- Execution begins after authentication middleware has confirmed the user's identity and put it in the request `context`, so every field resolver can see it.
- Authentication does not answer whether that user may see the data in each selected field; authorization is a separate check made once execution has begun.
- Authorization is business logic ("only authors can see their drafts"). Keep one source of truth in the business logic layer, not in the GraphQL layer: logic written inside resolvers must be duplicated for every entry point to the service and can drift so users see different data depending on which API they use. Inline resolver checks are fine for learning or prototyping.
- The resolver for a protected field calls a business-layer function (for example a repository method taking the user and the object) which returns the value or `null`.
- Pass the business layer a fully hydrated user object rather than an opaque token or API key, so authentication and authorization stay in separate stages.
- If you do enforce in the GraphQL layer, type system directives are one approach: declare something like `directive @auth(rule: Rule) on FIELD_DEFINITION` and apply it to fields. How the directive affects execution is up to your GraphQL implementation, and the rule itself should still be delegated to the business layer.

## Verify
- [ ] Every sensitive field has a check reachable from all entry points (GraphQL, REST, jobs) through the same business-layer function.
- [ ] Resolvers receive the user from `context`, not from raw request headers.

## Checked
2026-11-01. Confirmed against the GraphQL Learn "Authorization" page. Removed as unconfirmed by it: DataLoader-batched checks, specific nulling and error policies, OWASP and Apollo Server recommendations (those pages were not used to confirm claims; sources list trimmed to the page used).
Method: documentation only; no commands were run.
