---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.modular-monolith-design
name: modular-monolith-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, modular-monolith-design, modular-monolith, bounded-contexts, domain-driven-design, archunit]
level: practitioner
status: docs-checked
description: "Design a modular monolith: modules from bounded contexts, modular APIs and data storage, boundary tests with ArchUnit, and Fowler's monolith-first caveats."
sources: ["https://learn.microsoft.com/azure/architecture/microservices/model/domain-analysis", "https://www.archunit.org/userguide/html/000_Index.html", "https://docs.spring.io/spring-modulith/reference/", "https://martinfowler.com/bliki/MonolithFirst.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modular monolith

## When (Fowler, Monolith First)
Fowler's argument: successful microservice stories mostly started as a monolith that got too big;
microservices need good, stable boundaries (the task of drawing the right bounded contexts), and
even experienced architects struggle to get boundaries right at the start. He describes the logical
monolith-first approach as designing the monolith carefully, "paying attention to modularity within
the software, both at the API boundaries and how the data is stored", but says he would like more
success stories. He also warns you cannot assume an arbitrary system can be split: most acquire too
many dependencies between modules, and the gradual routes that worked needed a good modular design to start with.
The counter-argument he records: building a monolith modular enough to split takes a lot of discipline.

## Steps
1. **Find modules from the domain.** Microsoft's domain analysis flow is: analyse the domain, define
   bounded contexts, define entities, aggregates and services, then identify services. Mapping business
   functions can use event storming or a less formal whiteboard; the goal is shared understanding
   before choosing technology. A bounded context is where one domain model applies.
2. **Check ownership against teams.** If one team must own several unrelated bounded contexts, or one
   context needs coordination across many teams, revisit the boundaries or the team structure.
3. **Give each module a public API and hide internals** (Fowler: modularity at the API boundaries).
   Spring Modulith is described as an opinionated toolkit for domain-driven, modular Spring Boot
   applications; see its reference for its module rules.
4. **Enforce boundaries in tests.** ArchUnit expresses rules as code, for example
   `slices().matching("com.myapp.(*)..").should().beFreeOfCycles()` (the capture group makes one slice
   per sub-package) and `noClasses().that().resideInAPackage(...)...`. Run them in CI so violations fail the build.
5. **Keep data modular** (Fowler: how the data is stored). Do not let modules read each other's tables.

## Gotchas
- Without automated boundary checks, modularity erodes.
- Shared tables across modules make a later split hard.

## Verify
- [ ] Architecture tests run in CI and fail on cycles or forbidden dependencies.
- [ ] Each module's owners can be named.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed: Fowler's Monolith First text, the Microsoft domain-analysis flow, event storming and team
ownership guidance, the ArchUnit slices and noClasses examples, and the Spring Modulith one-line description.
Removed as not on the cited pages: Spring Modulith `verify()`, JPMS, .NET `internal`, NetArchTest,
dependency-cruiser, import-linter, transactional outbox, CODEOWNERS, and the extraction triggers.
