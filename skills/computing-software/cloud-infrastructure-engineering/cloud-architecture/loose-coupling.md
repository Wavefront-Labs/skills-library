---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.loose-coupling
name: loose-coupling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, loose-coupling, temporal-coupling, asynchronous-communication, queues, events, contract-versioning, coupling-analysis]
level: practitioner
status: draft
description: "Reduce coupling between components: identify temporal, location, data-format and deployment coupling, and apply queues, events, discovery, versioned contracts and owned data."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_prevent_interaction_failure_loosely_coupled_system.html", "https://learn.microsoft.com/azure/architecture/guide/design-principles/minimize-coordination"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loose coupling with queues and events

## Kinds of coupling and the fix
| Coupling | Symptom | Fix |
|---|---|---|
| Temporal | A fails when B is down/slow | queue/event between them; async request-reply |
| Location | hard-coded hosts/IPs | DNS/service discovery, LB endpoints, config |
| Data format | B breaks when A adds a field | versioned schemas, tolerant reader, additive changes only |
| Data ownership | shared DB tables | each service owns its data; expose API/events |
| Deployment | must release together | backward-compatible contracts, consumer-driven contract tests |
| Platform | specific runtime/SDK required | standard protocols (HTTP, AMQP, CloudEvents) |

## Steps
1. Draw the interaction graph; mark synchronous calls on critical paths.
2. For each sync call ask: does the caller need the answer now? If no → queue/event.
3. If yes → keep sync but add timeout, retry with budget, circuit breaker and a fallback.
4. Contracts: schema registry or OpenAPI with compatibility checks in CI.
5. Prefer choreography for notifications, orchestration for business processes with steps.

## Gotchas
- Asynchrony moves complexity to consistency and debugging (tracing, DLQs, idempotency).
- "Loose coupling" via a shared event schema owned by nobody — every event needs an owner.

## Verify
- [ ] Stopping a downstream non-critical service doesn't fail upstream requests.
- [ ] Contract checks run in CI for every producer.
