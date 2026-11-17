---
id: computing-software.messaging-and-integration.apache-camel.intercept
name: intercept
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, intercept, interceptfrom, intercept-send-to-endpoint, detour]
level: practitioner
status: docs-checked
description: "Camel intercept, interceptFrom and interceptSendToEndpoint: scope, onWhen, stop, skipSendToOriginalEndpoint, afterUri, URI pattern matching and intercepted exchange properties."
sources:
  - https://camel.apache.org/components/next/eips/intercept.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intercept

- `intercept`: runs before every processing step (two `to` steps means it fires twice).
- `interceptFrom`: only the incoming `from`. Applied to routes known at startup; not dynamic, so consumers created via the Java API do not trigger it.
- `interceptSendToEndpoint`: when an Exchange is about to be sent. Dynamic, so runtime-built URIs trigger it.

All can be global or in Route Configuration.

Shared options: `onWhen` (predicate) and `stop` (end routing, exchange completes successfully).

Only for `interceptSendToEndpoint`:
- `skipSendToOriginalEndpoint`: detour instead of sending.
- `afterUri`: send to another endpoint after the interceptor, e.g. to process the response.

Pattern matching tries exact URI, then wildcard (`*` at the end: `jms*`, `file:order/inbox/*`), then regex (`jms:queue:(gold|silver)`).

Exchange properties: `Exchange.INTERCEPTED_ENDPOINT`, `INTERCEPTED_ROUTE_ENDPOINT`, `INTERCEPTED_ROUTE_ID`, `INTERCEPTED_NODE_ID`.

Examples: `interceptFrom("jms*")` logs only JMS-sourced messages. `interceptSendToEndpoint("kafka*").skipSendToOriginalEndpoint().onWhen(simple("${header.biztype} == 'TEST'"))` keeps test messages out of Kafka (redirect to `mock:kafka`). With several matching interceptors, the sending route's run first, then the endpoint's own (e.g. from `mockEndpoints`).

Verify: a message sent to a `kafka*` endpoint with the skip option reaches the detour and not Kafka.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel intercept page: the three interceptor kinds and which are dynamic, global or Route Configuration scope, onWhen, stop, skipSendToOriginalEndpoint, afterUri, exact then wildcard then regex matching, the intercepted exchange property names, the jms* and kafka* examples and the ordering rule for several interceptors on one endpoint all match. No commands were run.
