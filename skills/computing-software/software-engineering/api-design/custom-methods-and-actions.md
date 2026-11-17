---
id: computing-software.software-engineering.api-design.custom-methods-and-actions
name: custom-methods-and-actions
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, custom-methods, actions, aip-136, http-methods, state-transitions]
level: practitioner
status: docs-checked
description: "Design custom methods (actions) that do not fit CRUD - cancel, approve, move - with Google AIP-136 colon syntax or action sub-resources, and when to model them as state instead."
sources:
  - https://google.aip.dev/136
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
  - https://cloud.google.com/apis/design/custom_methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom methods and actions

Resource-oriented APIs prefer standard methods (Get, List, Create, Update, Delete). Some operations do not map cleanly: cancel an order, approve a request, restart a VM, send an email, translate text.

## First, try to model it as state or a resource
- "Archive" -> `PATCH /documents/42 {"archived": true}` if it is just a field change with no extra semantics.
- "Approve" with history and approver -> create an `approvals` sub-resource: `POST /requests/42/approvals`.
- "Search" with complex criteria -> `List` with filters, or a `searches` resource for saved/long queries.
Use a custom method when the operation has side effects or semantics beyond setting a field (state machine transition with validation, triggering work).

## Google AIP-136 style
```
POST /v1/orders/123:cancel          body: {"reason": "customer request"}
POST /v1/instances/abc:restart
POST /v1/projects/p1/documents:batchGet     (collection-level custom method)
POST /v1:translateText                       (stateless method: verb and noun after the colon)
```
- The HTTP method must be GET or POST: GET for methods that only retrieve data or state, POST for anything with side effects, and POST may carry a retrieval whose payload could exceed URL limits.
- A `:` plus the custom verb in the URI, camelCase if words must be separated; the verb must match the verb in the RPC name. The method name is a verb followed by a noun and does not use the standard verbs (Get, List, Create, Update, Delete).
- When operating on a specific resource, the method may return the resource itself.

## Other conventions
- Action sub-path such as `POST /orders/123/cancel` is a common alternative; pick one convention per API and document it.
- Azure guidelines allow `:` in a path segment only to designate an action operation, and say a POST Action returns 200-OK with a body (even an empty object) so properties can be added later.

## Semantics to define
- Idempotency: is cancelling a cancelled order a no-op (success with current state) or an error? Prefer idempotent outcomes.
- Preconditions and errors: return a clear error for an invalid state transition that names the current state.
- Authorisation per action (separate permission `orders.cancel`), not just `orders.update`.
- Concurrency: support an etag precondition for actions that depend on current state.

## Verify
- [ ] OpenAPI documents each action with its allowed source states and error codes.
- [ ] Repeating the action is safe or explicitly rejected; tests cover both.

## Checked
2026-11-01. Confirmed in AIP-136: GET/POST rules, colon plus camelCase verb matching the RPC name, verb-noun naming, no standard verbs, stateless `:translateText` form, resource return. Confirmed in the Azure REST guidelines: `:` only for action operations; POST Action returns 200-OK with a body. Removed: GitHub/Stripe URL examples, 409/FAILED_PRECONDITION, Idempotency-Key, If-Match and problem-details specifics, request-message naming.
Method: documentation only; no commands were run.
