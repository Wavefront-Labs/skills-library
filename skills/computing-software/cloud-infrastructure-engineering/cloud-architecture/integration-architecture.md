---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.integration-architecture
name: integration-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, togaf, integration-architecture, sync-vs-async, api-led, event-streaming]
level: practitioner
status: draft
description: "Design an integration architecture: choose sync APIs, async messaging, event streaming or batch per interaction, with contracts, error handling and ownership."
sources: ["https://www.enterpriseintegrationpatterns.com/", "https://learn.microsoft.com/azure/architecture/guide/architecture-styles/event-driven", "https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-integrating-microservices/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integration architecture (sync vs async)

## Choose the style per interaction
| Need | Style |
|---|---|
| caller needs an answer now, short operation | synchronous API (REST/gRPC) |
| work can finish later, absorb spikes | queue (point-to-point) |
| many consumers react to a fact | pub/sub events |
| replayable ordered history, high volume | event streaming (Kafka, Kinesis, Event Hubs) |
| large periodic data sets | batch / file transfer, ELT |

## Steps
1. **List interactions** between systems from the dependency map with volume, latency need
   and consistency need.
2. **Default to async** across bounded contexts; keep sync calls within the latency budget
   and avoid chains of more than 2-3 synchronous hops.
3. **Contracts**: OpenAPI / AsyncAPI specs, schema registry for events, versioning rules
   (additive changes only; new version for breaking).
4. **Error handling**: timeouts, retries with backoff, idempotent consumers, dead-letter
   queues with an owner who watches them.
5. **Platform**: API gateway for external and cross-domain APIs; one managed broker family
   per use rather than many; iPaaS for SaaS-to-SaaS integration.
6. **Ownership**: producers own event schemas; integration is not a central team bottleneck.

## Gotchas
- Shared databases as integration couple everything; avoid.
- Async without observability (trace propagation through messages) makes failures invisible.

## Verify
- [ ] Each interface has a published contract and owner.
- [ ] DLQs have alerts and a runbook.
