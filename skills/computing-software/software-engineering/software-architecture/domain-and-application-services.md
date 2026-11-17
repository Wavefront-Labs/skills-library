---
id: computing-software.software-engineering.software-architecture.domain-and-application-services
name: domain-and-application-services
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, ddd, domain-services, application-services, use-cases, anemic-domain-model]
level: practitioner
status: verified
description: "Separate application services (use-case orchestration, transactions, auth) from domain services (stateless domain logic spanning aggregates) and avoid anemic models."
sources: ["https://www.domainlanguage.com/ddd/reference/", "https://martinfowler.com/bliki/AnemicDomainModel.html", "https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-application-layer-web-api-design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain services and application services

## Application service (use case)
Thin orchestration for one use case:
```python
class TransferFunds:
    def __init__(self, accounts, transfer_policy, uow, events): ...
    def __call__(self, cmd: TransferCommand, user):
        authorize(user, "transfer", cmd.from_id)
        with self.uow:                                   # transaction boundary
            src = self.accounts.get(cmd.from_id)
            dst = self.accounts.get(cmd.to_id)
            self.transfer_policy.transfer(src, dst, Money(cmd.amount, cmd.currency))
            self.uow.commit()
        self.events.publish_pending()
```
Owns: loading/saving aggregates, transactions, authorization, calling infrastructure (email,
queues), mapping DTOs. Contains **no business rules**; if you see `if balance < amount` here, it's
in the wrong place.

## Domain service
Stateless operation that is a domain concept but doesn't belong to one entity or value object,
usually because it spans aggregates or needs a domain policy:
- `TransferPolicy.transfer(src, dst, amount)` enforcing limits across two accounts.
- `PricingService.price(cart, promotions)`.
Named in the ubiquitous language, lives in the domain layer, depends only on domain types
(interfaces for anything external).

## Infrastructure service
Technical capability (email sender, payment gateway client) behind an interface the domain or
application layer defines.

## Avoiding the anemic domain model
Fowler's anti-pattern: entities as data bags with getters/setters, all logic in "services". Push
behaviour into entities and value objects first; reach for a domain service only when no single
object naturally owns the operation. Too many domain services = missing concepts.

## Tests
Domain services and entities: fast unit tests, no mocks needed. Application services: tests with
in-memory repositories and fakes, checking orchestration and transaction behaviour.
