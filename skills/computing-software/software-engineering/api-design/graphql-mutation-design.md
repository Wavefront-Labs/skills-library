---
id: computing-software.software-engineering.api-design.graphql-mutation-design
name: graphql-mutation-design
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-mutations, input-types, payload-types, idempotency]
level: practitioner
status: docs-checked
description: "Design GraphQL mutations as specific verbs with single input objects and payload types that return the changed object and user errors, and make them idempotent."
sources: ["https://graphql.org/learn/mutations/", "https://relay.dev/docs/guided-tour/updating-data/graphql-mutations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL mutation design

## Shape (illustrative convention)
```graphql
type Mutation {
  cartLineAdd(input: CartLineAddInput!): CartLineAddPayload!
}
input CartLineAddInput { cartId: ID!, merchandiseId: ID!, quantity: Int! = 1, clientMutationId: String }
type CartLineAddPayload {
  cart: Cart                       # the changed object, so clients update caches in one round trip
  userErrors: [UserError!]!        # expected business failures
  clientMutationId: String
}
type UserError { field: [String!], message: String!, code: CartErrorCode }
```

## Rules
- **Specific verbs over CRUD**: `orderCancel`, `orderMarkAsPaid` beat a generic `updateOrder(status:)`;
  each encodes one business action with its own validation and permissions.
- Name `nounVerb` (`cartLineAdd`) so mutations sort together by resource, or `verbNoun`; just be consistent.
- Use a dedicated Input Object type per mutation (graphql.org: a structured object instead of many scalar arguments) rather than sharing one input type between create and update.
- Purpose-built mutation fields let arguments be Non-Null, whereas a generic update mutation would need many nullable arguments (graphql.org).
- Return the mutated object (the specification does not say what a mutation returns; a payload object is common) so clients can update caches without refetch.
- Batch actions: one mutation taking a list of ids with per-item results, rather than clients sending N aliased mutations.
- Top-level fields on the Mutation type execute **serially**; fields on other types are often executed in parallel.

## Idempotency
Network retries re-send mutations. Accept an idempotency key (`input.idempotencyKey` or header) on
create/charge-style mutations and return the original result on replay.

## Verify
Schema lint can enforce input/payload naming; integration test that a duplicate submission with the same key creates one record.

## Checked
2026-11-01. Confirmed on graphql.org Mutations: Input Object types, purpose-built fields allow Non-Null arguments, spec leaves return type open (payload common), top-level mutation fields run serially. Removed: Shopify-specific shape claims (page not found), clientMutationId, graphql-js/Apollo absent-vs-null details, lint tool names, Relay/Apollo cache specifics. The SDL above is an illustrative convention, not a quoted standard.
Method: documentation only; no commands were run.
