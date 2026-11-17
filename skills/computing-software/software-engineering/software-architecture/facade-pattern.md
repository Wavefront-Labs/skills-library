---
id: computing-software.software-engineering.software-architecture.facade-pattern
name: facade-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, facade-pattern, gof, subsystem, simplified-interface, module-api, coupling]
level: practitioner
status: verified
description: "Use the GoF Facade to give a complex subsystem one simple entry point, reducing coupling, and avoid it turning into a god object."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Facade", "https://refactoring.guru/design-patterns/facade"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facade

**Intent (GoF):** provide a unified interface to a set of interfaces in a subsystem; a
higher-level interface that makes the subsystem easier to use.

## When it fits
- Callers need a common use case from a subsystem with many moving parts (video
  transcoding: probe, decode, filter graph, encode, mux).
- A module's public API: everything else stays internal, so the module can change.
- Wrapping a sprawling legacy subsystem before strangling it.

## Shape
```python
class CheckoutFacade:
    def __init__(self, carts, pricing, inventory, payments, orders, mailer): ...
    def place_order(self, cart_id: str, payment_token: str) -> OrderId:
        cart = self.carts.get(cart_id)
        quote = self.pricing.quote(cart)
        with self.inventory.reserve(cart.items) as reservation:
            charge = self.payments.charge(payment_token, quote.total)
            order = self.orders.create(cart, quote, charge)
            reservation.commit()
        self.mailer.send_confirmation(order)
        return order.id
```
Callers (HTTP handler, CLI) call one method; subsystem classes stay hidden.

## Facade vs related patterns
- Adapter: makes an existing interface match an expected one; Facade defines a new,
  simpler one.
- Application service (DDD/clean architecture): a facade per use case at the
  application layer.
- Module boundary: in a modular monolith, each module exposes a facade/API package;
  enforce with ArchUnit, Go `internal/`, or package visibility.

## Pitfalls
- God facade: one class with 60 methods for every use case. Split by use case or
  audience.
- Business rules creeping into the facade instead of the domain objects (it should
  orchestrate, not decide).
- Not optional: GoF notes clients may still use subsystem classes directly when they
  need power; for module boundaries you usually want to forbid that.

## Verify
- [ ] External callers import only the facade/API package (architecture test).
- [ ] Facade methods map 1:1 to use cases and contain orchestration only.
