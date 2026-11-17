---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.saga-pattern
name: saga-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, saga-pattern, saga, distributed-transactions, orchestration, choreography, compensating-transaction, step-functions, durable-functions, temporal, workflows, eventual-consistency]
level: advanced
status: docs-checked
description: "Keep data consistent across services without 2PC: choose orchestration vs choreography, design compensations and pivot steps, handle timeouts, and make every step idempotent."
sources: ["https://learn.microsoft.com/azure/architecture/reference-architectures/saga/saga", "https://microservices.io/patterns/data/saga.html", "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html", "https://docs.temporal.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saga

A saga is a sequence of local transactions; if step N fails, compensating actions undo steps 1..N-1
semantically (refund, release reservation) — there is no rollback.

## Design
1. **List steps and classify** (compensable, pivot, retryable, as in the Azure saga reference):
   - *Compensatable* — can be undone (reserve stock → release).
   - *Pivot* — the go/no-go point; after it the saga must complete (charge card).
   - *Retryable* — after the pivot; idempotent and must eventually succeed (send confirmation): retry with backoff and alert.
   Order steps so risky/compensatable ones come before the pivot.
2. **Orchestration vs choreography**
   - Orchestration (a coordinator such as Step Functions or Temporal): explicit state, easy to see where a saga is stuck. Prefer it as steps grow.
   - Choreography (services react to each other's events): fewer moving parts for 2-3 steps;
     becomes untraceable as it grows.
3. **Write compensations** per step, idempotent, and accept that they may fail too (retry; then
   human queue).
4. **Isolation anomalies**: other requests see intermediate state. Countermeasures: semantic
   locks (`status=PENDING`), commutative updates, re-read values before acting, version checks.
5. **Timeouts**: every waiting step has a deadline that triggers compensation.
6. **Correlation**: one saga id on every message and log line.

## Gotchas
- A compensation is a new business action (refund email), not a delete — the customer may see it.
- Orchestrators have execution-history limits (look up the limit for your engine) — split long sagas into child workflows.
- Choreography cycles: A reacts to B reacts to A. Draw the event flow before building.

## Checked
2026-10-28. Confirmed against the Azure saga reference architecture (pivot transaction as point of no return, compensable steps before it, retryable idempotent steps after it) and microservices.io saga pattern (orchestration versus choreography, compensating transactions, isolation anomalies and countermeasures). Removed: the Step Functions 25,000 event figure, the 15 min example, the "more than 3 steps" threshold and named-attribution of the step classes.
Method: documentation only; no commands were run.

## Verify
- [ ] Fault-inject failure at every step: final state is consistent (all done or all compensated).
- [ ] Replay the same command twice: no double charge.
- [ ] Dashboard lists sagas stuck > timeout.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.compensating-transaction, computing-software.cloud-infrastructure-engineering.cloud-architecture.idempotency
