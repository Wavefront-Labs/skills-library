---
id: computing-software.software-engineering.software-architecture.gateway-pattern
name: gateway-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, gateway-pattern, poeaa, external-integration, anti-corruption-layer]
level: practitioner
status: verified
description: "Wrap each external system or API behind a Gateway (PoEAA): domain-shaped interface, translation, error mapping, retries and a fake for tests."
sources: ["https://martinfowler.com/articles/gateway-pattern.html", "https://martinfowler.com/eaaCatalog/gateway.html", "https://martinfowler.com/bliki/SelfInitializingFake.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway for external systems (PoEAA)

A **Gateway** is an object that encapsulates access to an external system or resource (payment API,
message broker, legacy SOAP service, file drop). The rest of the code talks to the gateway in its
own terms.

## Design
```python
class PaymentGateway(Protocol):
    def authorize(self, amount: Money, card: CardToken, idem_key: str) -> Authorization: ...

class StripePaymentGateway:
    def authorize(self, amount, card, idem_key):
        try:
            pi = self._stripe.PaymentIntent.create(amount=amount.minor_units, currency=amount.currency.lower(),
                                                   payment_method=card.value, confirm=True,
                                                   idempotency_key=idem_key)
        except stripe.CardError as e:
            return Authorization.declined(reason=map_decline(e.code))
        except (stripe.APIConnectionError, stripe.RateLimitError) as e:
            raise PaymentUnavailable() from e
        return Authorization.approved(pi.id)
```
- Interface in domain language, defined by the consumer; one gateway per external system.
- Translate data both ways (vendor types never leak past it) and **map errors** into domain
  outcomes/exceptions.
- Put timeouts, retries with backoff, circuit breaker and logging of external calls here.
- stripe-python (16.0.0, run): `idempotency_key` is a request option, but `timeout=5` passed to `PaymentIntent.create` is not; it was sent to the API as a body parameter (`...&confirm=true&timeout=5`). Set the timeout on the HTTP client instead (`stripe.default_http_client = stripe.RequestsClient(timeout=5)`). Exceptions are importable as `stripe.CardError`, `stripe.APIConnectionError`, `stripe.RateLimitError`.
- For a big, messy external model this becomes an **anti-corruption layer** (DDD).

## Testing
- Unit tests use a fake implementation of the interface (in-memory, programmable outcomes).
- Contract/integration tests run the real gateway against the vendor sandbox or a recorded stub
  (WireMock, VCR.py, Pact) and check the same behaviours as the fake.

## Related patterns
Gateway is the generic idea; Table Data Gateway / Row Data Gateway apply it to database tables;
Fowler's 2021 article argues for one term "Gateway" for all external access wrappers, versus
Adapter (which adapts an existing interface to a specific required one).
