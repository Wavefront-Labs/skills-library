---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.monolith-decomposition
name: monolith-decomposition
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, monolith-decomposition, domain-driven-design, bounded-context, microservices-migration]
level: advanced
status: docs-checked
description: "Decompose a monolith into services using Dehghani's guide: start with a decoupled capability, minimise dependencies back, split data vertically, migrate in atomic steps."
sources: ["https://martinfowler.com/articles/break-monolith-into-microservices.html", "https://learn.microsoft.com/azure/architecture/microservices/model/domain-analysis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decomposing a monolith into services

## Steps (Zhamak Dehghani, "How to break a Monolith into Microservices")
1. **Check the destination first.** The guide says decomposition has a high overall cost and may take
   many iterations; evaluate whether it is the right path and whether microservices is the right destination.
2. **Warm up with a simple, fairly decoupled capability** (her retail examples: end-user authentication,
   then a customer-profile facade). Build the delivery pipelines, API management and operational
   readiness on these first, since failing to operate microservices is the biggest early risk.
3. **Minimise dependencies back to the monolith.** Decouple in the order that leaves dependencies
   pointing from the monolith to the new services (her example: promotions before buy). If a new service
   must call the monolith, expose a new monolith API and reach it through an anti-corruption layer.
4. **Split sticky capabilities early.** Leaky concepts such as web session couple many capabilities;
   break them into domain concepts and extract one at a time. She discourages a standalone session service.
5. **Decouple vertically and release the data early.** Extracting only the UI and facades while the data
   stays in one schema means "without decoupling the data, the architecture is not microservices".
   Move the capability with its data and redirect consumers to the new API; she cites Stripe's
   four-phase data migration strategy.
6. **Pick what matters and changes often.** Use commit history overlaid on the product roadmap.
7. **Decouple capability, not code.** She usually recommends rewriting and retiring old code over
   extracting it, except for relevant, clearly modelled, high-value code.
8. **Go macro first, then micro.** Find bounded contexts with DDD; avoid many anaemic CRUD services
   derived from the normalised data model. Start larger and split when teams are operationally ready.
9. **Migrate in atomic steps.** Each step builds the new service, redirects all consumers and retires the old
   code path; the anti-pattern is building the new service, using it for new consumers and never retiring the old.

## Finding boundaries (Microsoft domain analysis)
Analyse the domain, define bounded contexts, define entities, aggregates and services, then identify
services. Event storming is one structured way to map business functions. If one team must own several
unrelated bounded contexts, or one context needs many teams, revisit boundaries or team structure.

## Verify
- [ ] Each extracted capability owns its data and its consumers use the new API.
- [ ] The old code path is retired after each step.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.strangler-fig, computing-software.cloud-infrastructure-engineering.cloud-architecture.anti-corruption-layer

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on Dehghani's article and the Microsoft domain-analysis page. The AWS Prescriptive Guidance
source returned 404 and was removed together with its claims. Removed as not on the cited pages: strangler
facade routing, CDC-based data migration, event-storming code-coupling metrics, and the notification and
catalogue first-service examples.
