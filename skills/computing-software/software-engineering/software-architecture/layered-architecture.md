---
id: computing-software.software-engineering.software-architecture.layered-architecture
name: layered-architecture
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, layered-architecture, n-tier, clean-architecture, dependency-rule, sinkhole-anti-pattern]
level: practitioner
status: draft
description: "Design and enforce a layered (n-tier) architecture: layer responsibilities, open vs closed layers, the dependency rule, sinkhole anti-pattern and automated layer checks."
sources:
  - https://www.oreilly.com/library/view/software-architecture-patterns/9781098134280/
  - https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
  - https://www.archunit.org/userguide/html/000_Index.html#_layer_checks
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layered architecture

## Classic layers
| Layer | Owns | Must not |
|---|---|---|
| Presentation (UI, controllers, API handlers) | HTTP/CLI parsing, view models, auth context | contain business rules or SQL |
| Application / service | use-case orchestration, transactions, authorisation decisions | know HTTP or UI types |
| Domain / business | entities, rules, invariants | depend on frameworks or persistence |
| Persistence / infrastructure | repositories, ORM mapping, external clients | leak ORM types upward |
| Database | storage | |

## Closed vs open layers
- **Closed** (default): a request passes through each layer in order; presentation cannot call persistence directly. Gives isolation - you can replace the persistence layer without touching presentation.
- **Open:** a layer may be skipped (a shared utilities/services layer). Mark open layers explicitly; every unofficial skip erodes the structure.

## Dependency direction
Traditional n-tier points dependencies downward to the database, so the domain depends on persistence. Clean/Onion/Hexagonal invert this: the domain defines repository interfaces, infrastructure implements them, and dependencies point inward. Choose inversion when the domain is rich or persistence may change; keep plain layering for CRUD apps.

## Anti-patterns
- **Architecture sinkhole:** most requests pass through layers that do nothing but forward (controller -> service.getX() -> repo.getX()). Richards' rule of thumb: if more than ~20% of requests are pure pass-through, the layering is too strict or the app is CRUD - consider opening layers or a simpler style.
- Anaemic domain: all logic in services, entities are getters/setters.
- Layered monolith deployed as one unit scales and fails as one unit; layers are a code-organisation tool, not a deployment boundary.
- Package-by-layer (`controllers/`, `services/`, `repositories/`) spreads one feature across the tree; package-by-feature with layers inside each feature scales better.

## Enforcing it
- Java: ArchUnit `layeredArchitecture().consideringAllDependencies().layer("Web").definedBy("..web..")...whereLayer("Web").mayNotBeAccessedByAnyLayer()`; or JPMS/Gradle modules per layer.
- .NET: separate projects with references only downward (compiler-enforced), NetArchTest.
- Python: `import-linter` `layers` contract. TypeScript: `dependency-cruiser` forbidden rules, ESLint `boundaries` plugin.

## Verify
- [ ] Layer-check test runs in CI and fails on an upward or skip-layer import.
- [ ] Domain layer compiles without framework/ORM dependencies (if using inversion).
