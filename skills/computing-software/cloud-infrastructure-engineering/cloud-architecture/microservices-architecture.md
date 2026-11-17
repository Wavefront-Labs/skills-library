---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.microservices-architecture
name: microservices-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, microservices-architecture, microservices, service-boundaries, bounded-context, database-per-service, modular-monolith, distributed-monolith, conways-law, team-topologies]
level: advanced
status: docs-checked
description: "Decide if microservices fit and design them: bounded-context boundaries, private data, messaging, Fowler's prerequisites, and coupling symptoms from Microsoft's guide."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/microservices", "https://martinfowler.com/articles/microservices.html", "https://martinfowler.com/bliki/MicroservicePrerequisites.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microservices architecture

## Decide
Microsoft: each service is small, autonomous, owned by a single small team, kept in a separate codebase,
independently deployable and responsible for its own data; it implements a single business capability
within a bounded context. The benefits (independent deployment, small teams, fault isolation, independent
scaling, data isolation) come with challenges: complexity, hard testing and refactoring across service
boundaries, governance, latency from long call chains, data consistency (embrace eventual consistency,
BASE rather than ACID across services), a need for mature DevOps, versioning and skill set. Microsoft says
to evaluate whether the team has the skills and experience. Fowler's Monolith First article (cited in the
modular-monolith skill) argues for starting with a monolith.

## Prerequisites (Fowler, 2014)
Rapid provisioning (a new server in hours), basic monitoring (technical and business issues), and
rapid application deployment (a deployment pipeline of no more than a couple of hours), plus close
developer and operations collaboration. Start with a handful of services in production and learn before
adding more. Beyond a handful you need tracing of business transactions through multiple services, full
continuous delivery and product-centred teams.

## Design (Microsoft best practices)
1. Model services around the business domain; use DDD to find bounded contexts. Avoid overly granular services.
2. Data storage is private to the owning service; avoid sharing code or data schemas.
3. Communicate through well-designed APIs that model the domain, not the internal implementation.
4. Use messaging for asynchronous communication; Fowler warns that chained synchronous calls multiply
   downtime and cites the Guardian rule of one synchronous call per user request.
5. Loose coupling and high cohesion: things that change together should deploy together. Shared database
   schemas and rigid protocols cause coupling; chatty communication between two services may signal
   tight coupling and low cohesion.
6. Keep domain knowledge out of the API gateway.
7. Independent CI/CD pipelines per service; centralised logging, distributed tracing (OpenTelemetry) and metrics.
8. Conway's law (Fowler cites Melvin Conway, 1968): system design mirrors the organisation's communication structure, so align service boundaries with team boundaries.

## Antipatterns
Microsoft lists building without deep domain understanding (misaligned boundaries) and designing events
that depend on past or future events.

## Verify
- [ ] Every service has an owning team, its own pipeline and private data.
- [ ] Prerequisite capabilities (provisioning, monitoring, deployment) exist before the first service ships.
- [ ] No service reads another's database.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Microsoft architecture-style page, Fowler's prerequisites article and Fowler's
microservices article (synchronous calls, Conway's law). Removed as not on the cited pages: the Newman
book reference, consumer-driven contract tests (Pact), the "2-3 deep" call-chain limit, SLO and on-call
owner requirements, the percentage-of-coordinated-deploys target and the "merging is valid" advice.
