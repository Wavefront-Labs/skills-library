---
id: computing-software.software-engineering.software-architecture.repositories-and-factories
name: repositories-and-factories
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, ddd, repository-pattern, factory, aggregates, persistence-ignorance]
level: practitioner
status: docs-checked
description: "Implement DDD repositories (collection-like, per aggregate root), keeping the domain persistence-ignorant; testing, unit of work, and when to skip them."
sources: ["https://martinfowler.com/eaaCatalog/repository.html", "https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repositories (and where factories fit)

## Repository
Fowler (PoEAA): a Repository mediates between the domain and data-mapping layers using a collection-like interface; it acts like an in-memory collection of domain objects. Clients build query specifications declaratively and submit them to the repository; objects can be added and removed as with a simple collection and the encapsulated mapping code does the work. It concentrates query construction, which minimises duplicate query logic when there are many domain classes or heavy querying, and gives a one-way dependency between domain and data mapping.

Microsoft's .NET microservices guide, for DDD:
- The interfaces (abstractions) live in the domain model; implementations are persistence-specific adapters elsewhere (infrastructure layer).
- Define **one repository per aggregate root**, never one per database table. The aggregate root controls the aggregate's invariants and transactional consistency, so updates to the database should go only through repositories and aggregate roots.
- Querying through other channels is fine because queries do not change state: with CQS/CQRS, read-side queries can use plain SQL (for example Dapper) outside the domain model, unconstrained by aggregate rules.
- To make the convention explicit, constrain a generic repository base to aggregate roots, for example `IRepository<T> where T : IAggregateRoot`.
- Testing: keep repository interfaces in the domain layer and inject them, so unit tests can use mock repositories without a database. Tests against a real database are integration tests: have many fast unit tests and fewer integration tests.
- Versus a legacy data-access (DAL) class: a DAL class usually works at table/row level with little abstraction and tight coupling; a repository encapsulates persistence details and lets you add caching, logging and error handling through decorators or proxies, and swap adapters per environment.
- Unit of Work: a single transaction covering several insert/update/delete operations for one user action. EF Core's `DbContext` implements both Repository and Unit of Work (applied on `SaveChanges`). Unit of Work can be used with or without repositories.
- Repositories are not mandatory: they are useful but not critical to DDD in the way aggregates and a rich domain model are. Jimmy Bogard's feedback quoted on the page argues they hide persistence details, and with CQRS you may not need them.

## Factories
Not covered by the sources checked (the DDD Reference page cited earlier is only an index and returned no pattern text). Look up Evans' Factory pattern in the DDD Reference PDF before relying on any factory rule.

## Checked
2026-11-08. Confirmed against Fowler's Repository catalog entry and the Microsoft Learn page "Design the infrastructure persistence layer". Removed (not on those pages): the Java example and its named-query, no-generic-repository, transaction-ownership, Testcontainers and "40 finder methods" advice, and the whole factory section (creation versus reconstitution rules). The domainlanguage.com DDD Reference page was only an index and was dropped from sources.
Method: documentation only; no commands were run.
