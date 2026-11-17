---
id: computing-software.software-engineering.software-architecture.avoiding-two-phase-commit
name: avoiding-two-phase-commit
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, distributed-transactions, two-phase-commit, xa-transactions, sagas, outbox]
level: advanced
status: docs-checked
description: "Understand two-phase commit and XA, the risks of leaving transactions prepared, and choose sagas or the outbox instead across services."
sources: ["https://martinfowler.com/articles/patterns-of-distributed-systems/two-phase-commit.html", "https://microservices.io/patterns/data/saga.html", "https://www.postgresql.org/docs/current/sql-prepare-transaction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed transactions and why to avoid 2PC

## How 2PC works
Two phases: the **prepare** phase asks each node if it can promise to carry out the update; the **commit** phase actually carries it out. In prepare, each participant acquires what it needs (for example locks) so it can commit later, and promises the coordinator it can and will. If any node cannot promise, the coordinator tells all nodes to roll back, releasing locks, and the transaction aborts. Only if all agree does the commit phase start. Each participant must make its decision durable (for example with a write-ahead log) so a crashed node can complete the protocol after restart.

## PostgreSQL as an example participant
- `PREPARE TRANSACTION 'id'` stores the transaction state on disk and detaches it from the session; later `COMMIT PREPARED` or `ROLLBACK PREPARED` (from any session) finishes it.
- The identifier must be a string literal under 200 bytes and unique among prepared transactions.
- It is meant for an external transaction manager (such as X/Open XA systems), not for applications; unless you are writing a transaction manager you probably should not use it.
- Leaving a transaction prepared for a long time interferes with `VACUUM` reclaiming storage, can in extreme cases shut the database down to prevent transaction ID wraparound, and the transaction keeps holding its locks. List them in the `pg_prepared_xacts` view.
- If nothing tracks prepared transactions, keep the feature disabled by setting `max_prepared_transactions` to zero.

## Across services: sagas
In microservices with a database per service, the saga page lists "2PC is not an option" as a force. Implement each cross-service business transaction as a saga: a reliably coordinated sequence of local transactions; if a step fails on a business rule, compensating transactions undo the completed steps. Coordination is by choreography (each local transaction publishes events that trigger others) or orchestration (an orchestrator tells participants what to run).
- Drawbacks: no automatic rollback (you design compensating transactions) and no isolation (sagas can see data anomalies, so countermeasures are needed).
- To update its own database and publish a message atomically, a service cannot use a distributed transaction across database and broker; use event sourcing or the transactional outbox.
- A client that starts a saga with a synchronous request must be able to learn the outcome: respond when the saga completes, return an id and let the client poll, or return an id and notify the client later.

## Verify any alternative
Kill the process between each step in tests and check the system converges: no lost events, no double effects, compensations run.

## Checked
2026-11-08. Confirmed against Martin Fowler's Two-Phase Commit pattern page, the PostgreSQL PREPARE TRANSACTION page and the microservices.io Saga page. Removed (not on those pages): JTA and MSDTC, the "availability is the product of participants" line, Kafka and NoSQL XA support, the alternatives table (TCC, idempotent consumers, Kafka transactions, redesign), and the "when 2PC is acceptable" section including Spanner and CockroachDB. The Open Group XA PDF was not read.
Method: documentation only; no commands were run.
