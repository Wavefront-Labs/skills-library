---
id: computing-software.web-development.hasura.hasura-action-rest-connectors
name: hasura-action-rest-connectors
category: computing-software
field: web-development
product: hasura
tags: [hasura, actions, rest, kriti, request-transform, openapi]
level: advanced
status: docs-checked
description: "Call existing REST endpoints from Hasura Actions with request_transform using Kriti templates, without writing a handler, or import actions from OpenAPI."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/rest-connectors.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/open-api.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/api-reference/kriti-templating.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse a REST API as a GraphQL action with no custom service.

Availability: v2.1.0 and later. In the action definition add a `request_transform`:

```yaml
request_transform:
  template_engine: Kriti
  method: POST
  url: '{{$base_url}}/create_user'
  content_type: application/json
  query_params:
    id: "{{$session_variables['x-hasura-user-id']}}"
  body: '{"username": {{$body.input.username}}}'
```
Notes:
- `$base_url` is the action's configured handler URL; `$body.input.<arg>` reads action arguments (as in `$body.input.username`); `$session_variables` and `getSessionVariable(NAME)` read session variables; `$response.status` is available in response transforms.
- The same Kriti templating language is used by event trigger and cron trigger REST connectors, dynamic database connection routing and data connector config.
- Transforms can change the request method, URL, query parameters, headers and body, and a `response_transform` can reshape JSON responses.
- Use `escapeUri` to URL-encode templated values in the URL. Query params that evaluate to `null` are omitted.

OpenAPI import: in the Console use Import from OpenAPI on the Actions page, upload or paste a YAML or JSON spec, pick an operation and Create; the action definition is prepopulated (Base URL comes from `servers`).

Gotcha: the Console previews transforms but does not resolve server env vars or session variables, so enter mock values under Sample Context.

Debugging: with dev mode on, error responses include the `transformed_request` inside `extensions.internal`.

## Checked

2026-11-04. Confirmed against the cited pages: rest-connectors, open-api and Kriti pages and actions debugging: v2.1.0, request_transform fields, context variables, escapeUri, null query params, OpenAPI import flow, Kriti users list, transformed_request. Removed or corrected: `$body.input.id` example, the JSON-quoting gotcha and a vague OpenAPI claim.

Method: documentation only; no commands were run.
