---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.event-driven-architecture
name: event-driven-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, event-driven-architecture, eda, pub-sub, event-streaming, asyncapi, event-catalogue]
level: advanced
status: docs-checked
description: "Design an event-driven system: pub-sub vs event streaming, broker vs mediator topology, payload style, ordering, error handling, correlation IDs, schema evolution and fit."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/event-driven", "https://martinfowler.com/articles/201701-event-driven.html", "https://www.asyncapi.com/docs/reference/specification/latest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-driven architecture

## Pick the event style (Fowler)
- **Event notification**: the source tells others of a change and does not care much about any response.
- **Event-carried state transfer**: the event carries the data so consumers need not call back.
- **Event sourcing**: the event log is the record; supports audit and replay, but replay with outside interactions and
  schema change over time are problems.
- **CQRS**: separate data structures for reading and writing; it does not require events but is often combined with them.
Name which style each event uses.

## Publish-subscribe vs event streaming (Azure guide)
| | Publish-subscribe | Event streaming |
|---|---|---|
| Storage | not stored in a durable log; new subscribers do not see past events | written to a durable log, strictly ordered within a partition |
| Replay | no | clients read from any position and advance their own offset, so replay is possible |
| Azure service named | Event Grid | Event Hubs (high-throughput streaming) |

## Topology
- **Broker topology**: components broadcast events; simple, decoupled, no central coordination, but distributed
  transactions are risky because nothing can restart or replay them.
- **Mediator topology**: a mediator keeps state, handles errors and restarts and dispatches commands to channels,
  often queues; more control and consistency, but more coupling and a possible bottleneck.

## Steps
1. **Payload style**: full attributes (consumers need nothing else, but larger payloads, multiple systems of record,
   harder contracts) or keys only (single source of truth, but consumers query the source more).
2. **Document events and channels**: AsyncAPI describes the operations an application performs; the latest spec read was
   3.1.0. Keep a catalogue of event owner, schema and versions.
3. **Delivery**: run multiple consumer instances; make processing idempotent; ordering and exactly-once are hard with
   multiple instances. Persist in-transit events and dequeue only after acknowledgement to limit data loss.
4. **Error handling**: send failing events to an error-handler processor, then a dead-letter queue for inspection;
   resubmitted events are processed out of sequence. Use compensating transactions across services.
5. **Observability**: include a correlation ID in every event, planned from the start of the design.
6. **Schema evolution**: producers and consumers deploy independently; define a versioning strategy early and make
   consumers tolerate unknown versions.
7. **Event granularity**: too many fine-grained events overwhelm the system; over-consolidation causes needless processing.
8. **Security**: events are visible to many components; avoid unintended information exposure.

## When it hurts
Simple request-response flows, strong consistency across services, and teams without experience operating
asynchronous systems. Eventual consistency is a deliberate trade-off. For immediate answers use request and response
queues, which makes the flow effectively synchronous.

## Verify
- [ ] Every event type has an owner and a schema.
- [ ] A correlation ID lets one transaction be followed from producer through channel to consumer.
- [ ] Consumers handle duplicates and unknown schema versions.

## Checked
2026-11-08. Confirmed against the Azure event-driven architecture style page (pub-sub versus streaming, topologies,
payload approaches, challenges, when to use; page last updated 2026-03-07), Martin Fowler's "What do you mean by
Event-Driven?" (the four patterns, event-sourcing caveats, CQRS definition) and the AsyncAPI specification 3.1.0
(documents operations an application performs). Removed: broker and stream product comparisons beyond those named
by Azure, CloudEvents attributes, W3C traceparent, schema registry and CI checks, outbox (not on these pages).
Method: documentation only; no commands were run.
