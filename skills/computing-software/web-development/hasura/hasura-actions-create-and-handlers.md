---
id: computing-software.web-development.hasura.hasura-actions-create-and-handlers
name: hasura-actions-create-and-handlers
category: computing-software
field: web-development
product: hasura
tags: [hasura, actions, custom-business-logic, http-handler, debugging]
level: practitioner
status: docs-checked
description: "Define a Hasura Action as a custom GraphQL query or mutation backed by an HTTP handler, with the request payload, error contract and debugging tips."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/overview.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/create.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/action-handlers.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/debugging.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add custom business logic to the GraphQL API.

An Action has an SDL definition and a handler URL. In the Console: Actions -> Create, with types:

```graphql
type Mutation {
  insertAuthor(name: String!): AuthorOutput
}
type AuthorOutput { id: Int! }
```
Handler (POST) receives:

```json
{
  "action": { "name": "insertAuthor" },
  "input": { "name": "Alice" },
  "session_variables": { "x-hasura-role": "user" },
  "request_query": "mutation ..."
}
```
Session variable keys are lowercase.

Responses: a 2xx response with the output JSON is success. Errors use a 4xx status with a body like `{ "message": "<mandatory-error-message>", "extensions": { "code": "<optional-error-code>" } }`; `extensions` is an optional JSON object. A root-level `code` still works for backwards compatibility but `extensions.code` is preferred.

Useful options on the action definition: `timeout`, `forward_client_headers: true` and `headers` (for example an action secret from an env var, so the handler can reject other callers).

Debugging: start the server in dev mode (`HASURA_GRAPHQL_DEV_MODE=true`); on errors the response carries the webhook call details in `extensions.internal`, plus `transformed_request` inside `request` when transforms are used.

Gotcha: only actions of type mutation can be asynchronous.

## Checked

2026-11-04. Confirmed against the cited pages: create, action-handlers and debugging pages, async-actions page for the mutation-only rule, flags reference for HASURA_GRAPHQL_DEV_MODE. Removed or corrected: invented `validation-failed` code, the unsupported timeout unit and the Verify step.

Method: documentation only; no commands were run.
