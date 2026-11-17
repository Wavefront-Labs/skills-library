---
id: computing-software.software-engineering.software-architecture.strategy-pattern
name: strategy-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, strategy-pattern, gof, pluggable-algorithms, first-class-functions, open-closed-principle]
level: practitioner
status: verified
description: "Apply the Strategy pattern to swap algorithms at runtime: interface vs plain function, selection and injection, and when a lookup table or a simple if is the better choice."
sources:
  - https://refactoring.guru/design-patterns/strategy
  - https://en.wikipedia.org/wiki/Strategy_pattern
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strategy pattern

**Intent (GoF):** define a family of algorithms, encapsulate each one, and make them interchangeable so the algorithm varies independently of the clients that use it.

## Use it when
- Two or more ways to do one job (pricing rules, compression codecs, retry policies, sort orders) are chosen at runtime or per tenant.
- A method has a growing `switch` over "mode" and each branch is a full algorithm.
- You need to test the context with a fake algorithm.

## Shape
```python
from typing import Protocol

class ShippingCost(Protocol):
    def cost(self, order: "Order") -> Money: ...

class FlatRate:
    def __init__(self, amount: Money): self.amount = amount
    def cost(self, order): return self.amount

class ByWeight:
    def __init__(self, per_kg: Money): self.per_kg = per_kg
    def cost(self, order): return self.per_kg * order.weight_kg

class Checkout:
    def __init__(self, shipping: ShippingCost): self.shipping = shipping   # injected
    def total(self, order): return order.subtotal + self.shipping.cost(order)
```
In languages with first-class functions, a single-method strategy is just a function: `Checkout(shipping=lambda o: o.weight_kg * 2)`, `Comparator<T>`, `sort(key=...)`. Reach for a class only when the strategy carries configuration or several related methods.

## Selection
- Build the strategy at the composition root (DI container, factory, config) and inject it; the context should not `if` over strategy names.
- Registry for config-driven choice: `STRATEGIES = {"flat": FlatRate, "weight": ByWeight}`; fail loudly on an unknown key at startup, not on the first request.

## Pitfalls
- Strategies that need wildly different inputs: the interface degrades to a bag of optional arguments. Pass the context object or split the interface.
- One implementation forever: a speculative strategy interface is overhead; inline it until the second algorithm appears.
- Hidden state in strategies shared across threads; keep them stateless or create per use.

## Related
State (the object swaps its own behaviour as its state changes; Strategy is chosen from outside). Template Method varies steps by inheritance; Strategy varies the whole algorithm by composition. Fowler's Replace Conditional with Polymorphism often produces a Strategy.

## Verify
- [ ] Context tests use a fake strategy; each strategy has its own unit tests.
- [ ] Adding a new algorithm touches only a new class plus the registry/wiring.
