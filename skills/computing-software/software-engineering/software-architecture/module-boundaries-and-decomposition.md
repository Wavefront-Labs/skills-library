---
id: computing-software.software-engineering.software-architecture.module-boundaries-and-decomposition
name: module-boundaries-and-decomposition
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, modular-monolith, microservices, cohesion, coupling, bounded-context, domain-driven-design, ddd, dependency-rule, hexagonal-architecture, ports-and-adapters, archunit, import-linter, dependency-cruiser, spring-modulith, adr, architecture-decision-record, trade-off-analysis, atam, conways-law, team-topologies, fitness-functions, software-engineering]
level: advanced
status: draft
description: "Split a system into modules with high cohesion and low coupling, choose modular monolith vs microservices on evidence, enforce dependency rules in CI and record decisions as ADRs."
sources: ["Parnas, On the Criteria To Be Used in Decomposing Systems into Modules (1972)", "Evans, Domain-Driven Design (bounded contexts)", "Ford, Parsons, Kua - Building Evolutionary Architectures (fitness functions)", "Nygard, Documenting Architecture Decisions (2011)", "Skelton and Pais - Team Topologies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Module boundaries and decomposition — draw lines that make change cheap

**Goal:** decide where the seams go, how parts may depend on each other, and whether
those parts should be deployed separately, then keep the decision from eroding.

## 1. Find boundaries from change, not from layers
- Parnas's rule: each module hides one **design decision likely to change** (a data
  format, a vendor, a pricing rule). A module called `utils` or `services` hides nothing.
- Prefer **vertical slices by business capability** (`billing`, `catalogue`,
  `fulfilment`) over horizontal layers (`controllers`, `repositories`). A feature
  change should touch one slice, not every layer.
- Use DDD **bounded contexts**: where the same word means different things
  ("customer" in billing vs support), that's a boundary; each side owns its model.
- Mine version control for evidence of hidden coupling — files that change together
  belong together:
  ```
  git log --since=12.months --name-only --format='' | sort | uniq -c | sort -rn | head
  ```
  Tools such as code-maat or CodeScene compute change coupling between files.
- Test a candidate boundary: can you describe the module's public API in a few
  sentences? Would a typical feature need coordinated changes on both sides? If yes, merge.

## 2. Cohesion and coupling, concretely
- **High cohesion:** things that change for the same reason live together (the Single
  Responsibility idea applied at module level).
- **Low coupling:** prefer, in increasing strength of coupling: event/message →
  call through a narrow interface → shared types → shared database tables. Two modules
  writing the same table are one module wearing a disguise.
- Each module exposes a small **public API** (a package `api`/`index` file, a facade)
  and keeps everything else internal. Data crosses the boundary as DTOs/events, not
  ORM entities.
- Dependencies point toward stability and policy: domain code depends on nothing;
  adapters (HTTP, DB, queues) depend on the domain through ports (hexagonal / clean
  architecture). No cycles between modules.

## 3. Enforce the rules with tooling (fitness functions)
Rules in a wiki decay within months; rules in CI don't.
- Java/Kotlin: ArchUnit tests, e.g. `noClasses().that().resideInAPackage("..billing..")
  .should().dependOnClassesThat().resideInAPackage("..catalogue.internal..")`;
  Spring Modulith verifies module structure with `ApplicationModules.of(App.class).verify()`.
- Python: `import-linter` contracts (`layers`, `forbidden`, `independence`) in
  `.importlinter`, run as `lint-imports`.
- JS/TS: `dependency-cruiser` rules (`no-circular`, forbidden paths) or Nx
  `enforce-module-boundaries` with tags.
- .NET: NetArchTest or ArchUnitNET. Go: `internal/` directories are compiler-enforced.
- Separate build units (Gradle/Maven modules, workspace packages) give the strongest
  guarantee: an undeclared dependency doesn't compile.

## 4. Modular monolith vs microservices
Start with a **modular monolith** unless you have a concrete reason not to. Split a
module into a separate service only when at least one is true and measured:
- It needs **independent scaling** with a materially different resource profile.
- It needs a **different release cadence** and team ownership blocks on shared deploys.
- It has a different **failure/isolation or compliance** requirement (PCI scope, tenancy).
- It needs a different runtime or technology for a real reason.
Costs you are signing up for: network failure modes, distributed transactions (sagas,
outbox), eventual consistency, versioned contracts, distributed tracing, per-service
CI/CD and on-call. Conway's law: service boundaries that don't match team boundaries
generate constant cross-team coordination. A well-bounded modular monolith is the
cheapest path to services later; a tangled monolith split by network calls becomes a
**distributed monolith** — worst of both.

## 5. Trade-off analysis and ADRs
- Name the quality attributes that matter (latency, availability, modifiability,
  cost, time-to-market) and rank them; a decision is "good" only relative to that list.
- Compare at least two options in a short table against those attributes, including
  "do nothing". Note what each option makes hard to reverse.
- Record the outcome as an **ADR** (Nygard format): Title, Status (proposed / accepted /
  superseded by ADR-NNN), Context, Decision, Consequences. Keep them in the repo
  (`docs/adr/0007-split-billing-module.md`), numbered, immutable — supersede, don't edit.
  `adr-tools` or MADR templates help.

## Gotchas
- Shared "common" or "core" libraries quietly become the coupling hub; keep them tiny
  and free of business logic.
- Reporting and analytics queries joining across module tables silently re-couple
  everything; feed a read model or warehouse instead.
- Splitting a service along a boundary that still needs synchronous calls in both
  directions doubles latency and halves availability.
- Rule tools only check what you configured; new modules need adding to the contract.

## Verify
- [ ] Each module has a one-paragraph purpose and a deliberately small public API.
- [ ] No module reads or writes another module's tables directly.
- [ ] Dependency and cycle rules run in CI and fail the build on violation.
- [ ] Any service split cites a measured reason from section 4.
- [ ] Significant decisions exist as numbered ADRs with status and consequences.
- [ ] Change-coupling analysis shows most commits touch a single module.

Related: computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring
