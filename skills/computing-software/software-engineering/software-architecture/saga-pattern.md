---
id: computing-software.software-engineering.software-architecture.saga-pattern
name: saga-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, distributed-data, saga-pattern, orchestration, choreography, compensating-transactions, temporal]
level: practitioner
status: docs-checked
description: "Implement sagas for multi-service business transactions: orchestration vs choreography, compensating actions, pivot steps, idempotency and isolation anomalies."
sources:
  - https://microservices.io/patterns/data/saga.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sagas (orchestration and choreography)

A saga breaks a distributed transaction into a sequence of local transactions, one per service. Each completes atomically within one service, updates that service's database and starts the next step through an event or message. If a local transaction fails, compensating transactions reverse the changes of the preceding ones. With a database per service, ACID does not apply across stores, and two-phase commit is often a poorer fit than a saga.

## Example: place order (microservices.io)
- Choreography: Order service creates the order in PENDING and emits Order Created; Customer service tries to reserve credit and emits the outcome; Order service approves or rejects the order.
- Orchestration: Order service creates a saga orchestrator, which creates the order in PENDING, sends a Reserve Credit command to Customer service, receives the reply and approves or rejects the order.

## Choreography vs orchestration
| | Choreography | Orchestration |
|---|---|---|
| How | services exchange events with no central controller; each local transaction publishes domain events that trigger others | an orchestrator handles all transactions, tells participants what to do, stores task state and handles failure recovery with compensations |
| Good for | simple workflows with few services and no coordination logic; no single point of failure | complex workflows or adding services; avoids cyclic dependencies; clear separation of responsibilities |
| Drawbacks | confusing as steps are added; hard to track which commands each participant responds to; risk of cyclic dependency; integration testing needs all services running | coordination logic to implement; the orchestrator is a point of failure |

## Step types (Microsoft)
- **Compensable** transactions can be undone by transactions with the opposite effect.
- **Pivot** transaction: the point of no return; after it succeeds, compensable transactions no longer matter and every later action must complete. It can be the last compensable transaction or the first retryable one.
- **Retryable** transactions follow the pivot; they are idempotent and let the saga reach its final state despite transient failures.

## Considerations
- Handle transient failures and keep operations idempotent.
- Compensating transactions might not always succeed, which can leave the system inconsistent.
- Participants commit to their own databases, so changes cannot be rolled back, only compensated.
- A service must update its database and publish the message atomically; it cannot use a distributed transaction across database and broker, so use event sourcing or the transactional outbox (microservices.io).
- Debugging is complex and grows with the number of services; monitor and track saga workflows.
- A client that starts a saga with a synchronous request must learn the outcome: respond on completion, return an id to poll, or notify later.
- Not suitable when transactions are tightly coupled, when compensating transactions occur in earlier participants, or with cyclic dependencies.

## Isolation anomalies
No isolation across services, so: lost updates, dirty reads, fuzzy (nonrepeatable) reads. Countermeasures listed by Microsoft: semantic lock (an application-level flag that an update is in progress), commutative updates, pessimistic view (reorder so updates happen in retryable transactions, avoiding dirty reads), reread values before updating, version files (a log of operations on a record applied in the right order), and risk-based concurrency (sagas for low-risk updates, distributed transactions for high-risk ones).

## Verify
- [ ] Tests inject failure at every step and assert compensations run and the final state is consistent.
- [ ] Duplicate delivery of a message causes no double effect.

## Checked
2026-11-08. Confirmed against the microservices.io Saga page and the Microsoft Learn Saga pattern page (the old reference-architectures URL redirects to /patterns/saga). Removed (not on those pages): the payment and inventory example flow, the tools row (Kafka, Temporal, Step Functions, Camunda, Axon, MassTransit), "order risky steps last", the dedupe-by-saga-id advice, the timeout and stuck-saga dashboard advice. The Temporal docs landing page was dropped from sources.
Method: documentation only; no commands were run.
