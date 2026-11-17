---
id: computing-software.software-engineering.api-design.graphql-error-handling
name: graphql-error-handling
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-errors, result-unions, error-extensions, user-errors]
level: practitioner
status: docs-checked
description: "Handle GraphQL errors: what belongs in the top-level errors array with extensions codes versus typed result unions or userErrors fields, and partial data."
sources: ["https://spec.graphql.org/October2021/#sec-Errors", "https://www.apollographql.com/docs/apollo-server/data/errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL error handling

## Two kinds of failure
| Kind | Example | Where |
|---|---|---|
| Unexpected / system | DB down, resolver bug, auth missing, query invalid | top-level `errors` array |
| Expected / domain | card declined, username taken, out of stock | in the schema: `userErrors` or result union |

## Top-level errors
```json
{"data": {"order": null},
 "errors": [{"message": "Not authorized", "path": ["order"], "locations": [{"line":2,"column":3}],
             "extensions": {"code": "FORBIDDEN"}}]}
```
- Monitor the `errors` array, not only HTTP status codes; check how your server maps errors to status codes.
- A field error on a non-null field propagates to the parent field, resolving to null where allowed (spec, Handling Field Errors). Over-using `!` turns one bad field into an empty page.
- Use `extensions.code` with a fixed vocabulary (Apollo documents `UNAUTHENTICATED`, `FORBIDDEN`, `BAD_USER_INPUT`, `INTERNAL_SERVER_ERROR`). Clients branch on codes, never on messages.
- Mask internal errors in production: Apollo Server has a `formatError` hook run on each error before it is returned, and an `includeStacktraceInErrorResponses` option; log the original error.

## Domain errors in the schema
```graphql
union CheckoutResult = CheckoutSuccess | PaymentDeclined | OutOfStock
type PaymentDeclined { reason: DeclineReason!, retryable: Boolean! }
```
Unions make errors typed and discoverable; clients must handle `__typename`, so add a common
`interface Error { message: String! }` and tell clients to fall back on it for new members.
The simpler `userErrors: [UserError!]!` payload field works well for mutations.

## Checked
2026-11-01. Confirmed: GraphQL spec (non-null field errors propagate to the parent field), Apollo Server errors page (extensions.code values, formatError, includeStacktraceInErrorResponses). Removed: GraphQL-over-HTTP media type and status-code claims, spec section number, Shopify attribution, productionreadygraphql source.
Method: documentation only; no commands were run.
