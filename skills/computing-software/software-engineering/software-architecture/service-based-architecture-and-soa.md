---
id: computing-software.software-engineering.software-architecture.service-based-architecture-and-soa
name: service-based-architecture-and-soa
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, service-based-architecture, soa, coarse-grained-services, distributed-architecture]
level: practitioner
status: draft
description: "Apply service-based architecture: a handful of coarse-grained domain services sharing a database, as a step between monolith and microservices; contrast with classic SOA."
sources: ["https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://martinfowler.com/articles/microservices.html", "https://www.oreilly.com/library/view/software-architecture-the/9781492086888/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service-based architecture and SOA

## Service-based architecture (Richards & Ford)
- 4-12 **coarse-grained domain services** (Order, Fulfilment, Billing, Customer), each a separately
  deployed unit containing its full layered stack.
- Usually **one shared database** (or a few), optionally with per-service schemas and logical
  partitioning of tables.
- Separate UI(s) call services directly or via a thin API layer.
- ACID transactions stay inside one service; fewer distributed-transaction problems than
  microservices.

## When it's the right answer
- Monolith too big to deploy safely, but microservices' operational cost (dozens of services, data
  ownership, sagas) isn't justified.
- Domain decomposes into a few clear areas; teams are a handful.
- Migration step: carve the monolith into domain services first; split further only where scaling
  or team autonomy needs it.

## Design notes
- Draw service boundaries along domain/bounded contexts, not technical layers.
- Shared database risks: schema changes ripple. Mitigate with per-service schemas, shared tables
  owned by one service, and a federated "shared entity library" versioned carefully.
- Inter-service calls should be rare; frequent chatty calls mean wrong boundaries.
- Fault tolerance moderate: one service down doesn't kill others, but the shared DB is a common
  failure point.

## Classic SOA (contrast)
Enterprise-wide orchestration: business services, enterprise services, an **enterprise service bus**
doing routing, transformation and orchestration, canonical data models. Maximised reuse, but
coupling to the ESB and canonical model made change slow. Lessons kept: contracts and service
thinking. Lessons dropped: smart pipes (prefer smart endpoints, dumb pipes), enterprise-wide
canonical models.
