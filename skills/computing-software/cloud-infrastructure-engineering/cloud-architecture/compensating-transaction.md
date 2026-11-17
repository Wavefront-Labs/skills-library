---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.compensating-transaction
name: compensating-transaction
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, compensating-transaction, undo, semantic-rollback, eventual-consistency, workflow-recovery, idempotent-compensation]
level: advanced
status: docs-checked
description: "Design the undo steps for multi-step cloud operations: application-specific compensations, recorded progress, idempotent retryable undo, irreversible steps and human escalation."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/compensating-transaction", "https://microservices.io/patterns/data/saga.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compensating transaction

For an eventually consistent operation spanning data stores or services that cannot share an atomic transaction, record
information about each step and how to undo it. If the operation fails, the workflow rewinds through the completed
steps and reverses each. You often cannot simply restore the original state, because concurrent instances may have
changed the data; the compensation must account for concurrent work, and is application specific.

## Steps
1. **Design the undo with each step.** Record, as each forward step succeeds, both its execution state and its
   compensating action (the Azure example stores them in Cosmos DB), so the workflow can be resumed, correlated and
   audited.
2. **Retry first.** Treat step failures as transient and retry; compensate only when retries are exhausted or the
   failure is nontransient. Business rules may prefer an alternative path (another hotel) over rolling back.
3. **Compensations are business-specific**: cancelling a flight may not entitle the customer to a full refund. A
   compensation does not necessarily return data to its starting state; it compensates for the work completed.
4. **Idempotent and resumable**: compensating transactions can fail, steps may be retried, so make each an idempotent
   command and record progress to resume from the point of failure.
5. **Order**: not always the exact reverse. If one store is more sensitive to inconsistency, undo it first; some undo
   steps can run in parallel.
6. **Points of no return**: identify irreversible steps (external side effects, legally binding actions) and place
   them only after all critical validations succeed.
7. **Escalation**: when manual intervention is the only recovery, raise an alert with detailed failure reasons. In the
   Azure example, exhausted retries move the message to a dead-letter queue and raise an alert with correlation IDs.
   For high-impact or ambiguous cases, pause for human review; the customer, not the system, should decide to cancel
   in the travel example.

## Gotchas
- A blocked step may not fail visibly: use a timeout mechanism.
- Infrastructure must not lose the information needed to compensate, and must be resilient in both the original
  operation and the compensation; correlate and audit both end to end.
- Short-term locks with a timeout on required resources, acquired in advance, can raise success rates.
- Not suitable if retries alone suffice, or if the system cannot tolerate temporary inconsistency or compensation
  cannot restore a valid state; use atomic transactions instead.
- Saga (microservices.io) is the closely related pattern: a sequence of local transactions with compensating
  transactions, coordinated by choreography or an orchestrator; there is no automatic rollback, so developers must
  design the compensations.

## Verify
- [ ] Fail at each step in a test: all prior steps are compensated, in the intended order.
- [ ] Kill the coordinator mid-compensation: restart finishes it.
- [ ] The dead-letter or manual-intervention path has an owner and an alert.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.saga-pattern

## Checked
2026-11-08. Confirmed against the Azure Compensating Transaction pattern page (recorded steps and undo info,
application-specific compensation, retries before compensation, idempotent steps, ordering, irreversible steps,
manual intervention and alerts, timeouts, locks, when to use or avoid, Cosmos DB/Service Bus/dead-letter example)
and the microservices.io Saga page (local transactions, choreography versus orchestration, no automatic rollback).
Removed as not stated: "uncompensatable step must be last (pivot)", an N-retry escalation threshold, existence
check before delete, IaC roll-forward remark, pending/reserved-state advice.
Method: documentation only; no commands were run.
