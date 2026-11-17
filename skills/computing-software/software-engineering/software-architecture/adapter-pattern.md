---
id: computing-software.software-engineering.software-architecture.adapter-pattern
name: adapter-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, adapter-pattern, gof, wrapper, third-party-integration, ports-and-adapters]
level: practitioner
status: verified
description: "Use the GoF Adapter to make a third-party or legacy interface fit the interface your code expects, isolating vendor types and translation logic in one place."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Adapter", "https://refactoring.guru/design-patterns/adapter", "https://alistair.cockburn.us/hexagonal-architecture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adapter

**Intent (GoF):** convert the interface of a class into another interface clients expect.

## When it fits
- Integrating a vendor SDK (payment provider, email service) whose API shape and types
  you don't want spreading through your code.
- Making a legacy class satisfy a new interface without modifying it.
- The "adapters" in ports-and-adapters architecture are exactly this at system scale.

## Shape (object adapter: composition)
```typescript
// Port: what OUR code wants
interface PaymentGateway {
  charge(customerId: string, paymentMethodId: string, amount: Money): Promise<ChargeResult>;
}

// Adapter: wraps the vendor SDK
class StripeGateway implements PaymentGateway {
  constructor(private readonly stripe: Stripe) {}
  async charge(customerId: string, pmId: string, amount: Money): Promise<ChargeResult> {
    try {
      const pi = await this.stripe.paymentIntents.create({
        customer: customerId, payment_method: pmId, amount: amount.minorUnits, currency: amount.currency.toLowerCase(), confirm: true,
      });
      return { ok: true, reference: pi.id };
    } catch (e) {
      if (e instanceof Stripe.errors.StripeCardError) return { ok: false, reason: "declined" };
      throw new GatewayUnavailable("stripe", { cause: e });
    }
  }
}
```
With `confirm: true` and no `payment_method`, Stripe falls back to the customer's legacy `default_source` and recommends passing `payment_method` explicitly, so the port carries one. (Type-checked with `tsc --strict` against stripe-node.) The adapter translates: method names, argument shapes, units (minor units, lowercase
currency), errors (vendor exceptions -> domain results/exceptions), and ids.

Class adapter (inheriting from the adaptee) is possible in languages with multiple
inheritance; prefer composition.

## Rules
- Vendor types never appear in the port interface.
- Keep adapters thin: translation only, no business rules.
- Write contract tests for the adapter against the real service (sandbox) and use a
  fake implementation of the port in unit tests.

## Related
Facade simplifies a subsystem with a NEW interface; Adapter makes an EXISTING interface
conform to an expected one. An anti-corruption layer (DDD) is a set of adapters and
translators protecting a domain model from another model.

## Verify
- [ ] grep shows vendor SDK imports only inside adapter modules.
- [ ] Swapping the adapter for a fake requires no change to callers.
