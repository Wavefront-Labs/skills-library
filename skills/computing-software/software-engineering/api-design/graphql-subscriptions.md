---
id: computing-software.software-engineering.api-design.graphql-subscriptions
name: graphql-subscriptions
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-subscriptions, websockets, graphql-ws, pubsub]
level: advanced
status: docs-checked
description: "Design GraphQL subscriptions: the one-root-field rule from the spec and the graphql-transport-ws message flow, close codes and operation-id rules over WebSockets."
sources:
  - https://spec.graphql.org/October2021/#sec-Subscription
  - https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL subscriptions

**Goal:** define subscriptions that follow the spec and the graphql-ws protocol.

## Spec rules (October 2021)
- A subscription operation must have exactly one root field, which must not be an introspection field; `__typename` may not be a root field of a subscription.
- A document may contain several subscription operations, each with its own root field; when it does, the operation name must be given at execution.
- Executing a subscription maps an underlying Source Stream to a returned Response Stream; each response event is the result of executing the operation for each new source event.

```graphql
type Subscription { orderStatusChanged(orderId: ID!): Order! }
```

## graphql-ws protocol (subprotocol `graphql-transport-ws`)
- Client opens the WebSocket with sub-protocol `graphql-transport-ws` and sends `connection_init` (optional payload); operations are allowed only after the server acknowledges the connection, otherwise the socket closes with `4401: Unauthorized`.
- To reject a connection, for example when authentication fails, the protocol recommends closing the socket with `4403: Forbidden`.
- `subscribe` starts an operation with a unique operation id; if an active subscriber with that id exists, the server must close the socket with `4409`. Ids can be reused after an operation completes.
- Server sends `next` per result, then `complete`; if the server sent an `error` for the original subscribe, no `complete` follows. The client sends `complete` to stop listening; both sides must tolerate (and ignore) messages for operations they consider already completed.
- `ping` and `pong` messages may carry an optional payload. A message of an unspecified type or format closes the socket with `4400`.

## Verify
- [ ] Each subscription operation has exactly one non-introspection root field.
- [ ] Client and server agree on the `graphql-transport-ws` sub-protocol.

## Checked
2026-11-01. Confirmed against the GraphQL spec (October 2021) subscription sections and the graphql-ws PROTOCOL.md. Removed as unconfirmed by those pages: transport comparison with the legacy library and SSE, pub/sub and Redis server code, per-event authorization advice, outbox and load-balancer guidance, polling comparison.
Method: documentation only; no commands were run.
