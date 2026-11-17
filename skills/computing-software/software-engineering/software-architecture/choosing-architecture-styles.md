---
id: computing-software.software-engineering.software-architecture.choosing-architecture-styles
name: choosing-architecture-styles
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, monolith, modular-monolith, microservices, event-driven-architecture, conway-law, distributed-systems, service-boundaries, architecture-decision]
level: sme
status: draft
description: "Choose monolith, modular monolith, microservices, or event-driven architecture based on team topology and actual coupling, not industry fashion."
sources: ["Martin Fowler - MonolithFirst, Microservices Prerequisites", "Team Topologies (Skelton & Pais)", "personal experience migrating a monolith toward service boundaries"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing architecture styles — match the structure to the team, not the trend

**Goal:** pick monolith / modular monolith / microservices / event-driven for the
actual reason those trade-offs exist (team autonomy, deploy independence, failure
isolation) rather than because it's what a conference talk described.

## 1. Default: a modular monolith
One deployable, one process (or a small number), but with enforced internal module
boundaries (see
computing-software.software-engineering.software-architecture.module-boundaries-and-decomposition)
— no cross-module DB access, communicate through explicit interfaces. This gets most
of microservices' maintainability benefit (can't reach into another module's
internals) with none of the distributed-systems cost (network calls, partial
failure, eventual consistency, distributed tracing, N deploy pipelines). Most teams
under ~2 dozen engineers should start here and stay here until a specific pain
justifies splitting.

## 2. Microservices solve an organizational problem, not a technical one
The actual justification is **independent deployability across team boundaries**
(Conway's Law: your system's boundaries will mirror your org chart whether you plan
it or not) — team A ships without coordinating a release with team B, and a crash in
one service doesn't take down another. If there's one team (or a few teams that
deploy together anyway), splitting into services adds: network latency and partial
failure handling, distributed transactions/eventual consistency, N times the
operational surface (logging, monitoring, deploy pipeline, on-call) for the same
logic, and cross-service debugging. Pay this cost only when the org-boundary problem
is real — more than one team that needs to ship independently and whose coupling
through a shared deploy is the actual, observed bottleneck.

## 3. Event-driven architecture: decoupling at the cost of traceability
Services communicate via events (a queue/broker — Kafka, SQS, RabbitMQ) rather than
direct calls. Justified when: a producer shouldn't know or care who consumes an event
(true pub/sub fan-out), when a workflow spans unreliable downstream systems that
shouldn't block the producer (retry/backoff lives in the consumer, not the caller's
request path), or when audit/replay of history (event sourcing) is itself a
requirement. Cost: a request's effect is no longer traceable by reading one call
stack — debugging requires a correlation ID threaded through every hop and, usually,
distributed tracing from day one or the system becomes undebuggable the first time
something goes wrong. Avoid it for a simple request/response relationship where
synchronous is correct and simpler — "event-driven" is not automatically more
scalable than a direct call that a load balancer and more instances handle fine.

## 4. The migration path, if you do split
Don't big-bang rewrite. Extract one service at a time from the modular monolith,
starting with the module that has the clearest boundary and the strongest
independent-deploy need (often: the one a different team owns, or the one with
distinct scaling characteristics — e.g. a CPU-heavy job queue separated from a
request-serving API). The Strangler Fig pattern (route an increasing slice of traffic
to the new service while the monolith still serves the rest) avoids a long
feature-freeze during the migration.

## 5. Signals you picked wrong
- **Monolith pain**: deploys are blocked by unrelated teams' changes; one team's bug
  takes down an unrelated feature; the codebase has module boundaries nobody actually
  enforces (grep shows cross-module DB table access everywhere).
- **Microservices pain** (over-split): every feature touches 4 services and a
  distributed trace; local dev requires running 15 services via docker-compose;
  on-call rotation effectively requires knowing the whole system anyway because
  nothing fails in isolation; teams keep merging services back together.
- **Event-driven pain** (over-applied): nobody can answer "what happens when a user
  clicks X" without reading 5 consumers' code and a dead-letter queue; ordering bugs
  recur because events arrived out of order and nothing enforced an order.

## Gotchas
- "We might need to scale this independently later" is not sufficient justification
  on its own — a modular monolith with clean internal boundaries can be split later
  with much of the design work already done; splitting speculatively up front usually
  guesses the boundaries wrong anyway.
- Shared database across "microservices" is not microservices — it's a distributed
  monolith with all the network cost and none of the independent-deploy benefit
  (schema changes still require coordinating every service touching that table).
- Team size changes over time; an architecture chosen for a 40-person org doesn't
  automatically fit after layoffs/reorg down to 8 — revisit, don't assume it still fits.

## Verify
- [ ] The stated justification for the chosen style names a specific organizational
      or failure-isolation need, not "best practice" or "what's modern."
- [ ] If microservices: each service has its own datastore (or a clearly justified
      exception), confirmed by checking for cross-service table access.
- [ ] If event-driven: a request's full effect can be traced end-to-end via a
      correlation ID across every consumer, verified on at least one real trace.
- [ ] Module boundaries inside the monolith (if that's the choice) are enforced by
      tooling (import-linter, dependency-cruiser), not just convention.

Related: computing-software.software-engineering.software-architecture.module-boundaries-and-decomposition,
computing-software.software-engineering.api-design.rest-resource-design-and-versioning
