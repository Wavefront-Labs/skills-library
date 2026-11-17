---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.hexagonal-architecture
name: hexagonal-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, hexagonal-architecture, ports-and-adapters, clean-architecture, dependency-inversion, testability, cloud-portability]
level: practitioner
status: draft
description: "Structure services as hexagonal (ports and adapters): domain core free of cloud SDKs, ports for inbound/outbound, adapters per technology, enabling tests and provider swaps."
sources: ["https://alistair.cockburn.us/hexagonal-architecture/", "https://learn.microsoft.com/azure/architecture/microservices/model/tactical-ddd", "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hexagonal / ports and adapters

## Structure
- **Domain core**: business logic and entities; no framework, database or cloud SDK imports.
- **Ports**: interfaces the core defines - inbound (use cases, e.g. `PlaceOrder`) and outbound
  (e.g. `OrderRepository`, `PaymentGateway`, `EventPublisher`).
- **Adapters**: implementations - inbound (HTTP controller, queue consumer, Lambda handler) and
  outbound (DynamoDB repository, Stripe client, SNS publisher).
- Dependencies point inward; wiring at the composition root.

## Benefits in cloud systems
- Same core runs behind API Gateway + Lambda, containers or a CLI: only inbound adapters differ.
- Test the core with in-memory adapters; contract-test adapters against real services/emulators.
- Swap providers (queue, DB) by writing a new adapter.

## Steps
1. Identify use cases; define inbound ports as application services.
2. Define outbound ports by what the domain needs ("save order", not "PutItem").
3. Implement adapters; keep mapping between domain objects and persistence models in adapters.
4. Enforce dependency rules with architecture tests (ArchUnit, import-linter).

## Gotchas
- Leaky ports shaped like a vendor API, giving no portability.
- Over-abstraction for simple CRUD services; use where domain logic justifies it.

## Verify
- [ ] Core module has no cloud SDK dependencies (build check).
- [ ] Core tests run without network.
