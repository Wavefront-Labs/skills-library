---
id: computing-software.messaging-and-integration.apache-camel.saga
name: saga
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, saga, compensation, lra, long-running-action]
level: advanced
status: docs-checked
description: "Camel Saga EIP: propagation modes, completionMode AUTO or MANUAL, timeouts, compensation and completion routes, LRA header and services."
sources:
  - https://camel.apache.org/components/next/eips/saga-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saga

Groups actions so they all complete or are compensated; consistency holds only at the end.

Propagation (default `REQUIRED`: join the existing saga or create one): `REQUIRES_NEW` (always a new saga, old one suspended then resumed), `MANDATORY` (a saga must already exist, which is joined), `SUPPORTS` (join if one exists), `NOT_SUPPORTED` (an existing saga is suspended and resumed afterwards), `NEVER` (must not run inside a saga).

`completionMode`: `AUTO` (default; saga ends when the exchange that created it is done) or `MANUAL` (long-running; finish with `saga:complete` or `saga:compensate`).

`timeout`: no default; without one a failed saga can stay open indefinitely, so set one. On expiry the saga is canceled and compensated. Participant and saga timeouts can both be set; the earliest deadline wins.

Endpoints: `compensation` (undo; should not fail, retried on error), `completion` (runs on success; may be called more than once), `option` (values registered on the saga and passed to those routes as headers).

Header `Long-Running-Action` carries a globally unique saga id on every exchange, including compensations.

Services:
- `InMemorySagaService`: not for production, no persistence, no remote propagation.
- `LRASagaService`: MicroProfile LRA based; needs an external coordinator (Narayana suggested) and a REST context such as Undertow; exposes `/lra-participant`; an optional callback secret signs callbacks, bad signatures get 403.

Best practice: idempotent compensations, commutative actions and compensations, and completion handlers that tolerate duplicates.

Verify: when the saga is canceled (error or timeout), the `refundCredit` compensation route runs.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://camel.apache.org/components/next/eips/saga-eip.html.
Removed unconfirmed claims (sagaService option, completion must not fail, AUTO compensates on exception); reworded propagation modes to match the page. No commands were run.
