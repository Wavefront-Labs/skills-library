---
id: computing-software.qa-testing-engineering.test-automation.test-data-builders-and-factories
name: test-data-builders-and-factories
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-data-builders, factory-boy, test-data-management, object-mother, fishery, test-data]
level: practitioner
status: verified
description: "Create test data with builders and factories (factory_boy, Fishery, Java builders): sensible defaults, per-test overrides, related objects and unique sequences."
sources:
  - https://factoryboy.readthedocs.io/en/stable/
  - https://github.com/thoughtbot/fishery
  - http://www.natpryce.com/articles/000714.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test data factories and builders

**Goal:** each test states only the data that matters to it; everything else gets valid defaults. Replaces brittle shared fixtures and object mothers.

## Python: factory_boy
```python
import factory
from myapp.models import User, Order

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f"user{n}@example.test")
    name = factory.Faker("name")
    is_active = True

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    user = factory.SubFactory(UserFactory)
    total = 100
    class Params:
        refunded = factory.Trait(status="refunded", total=0)

def test_refund_hides_invoice():
    order = OrderFactory(refunded=True)     # only the relevant detail is visible
```
- `build()` (no DB), `create()` (saved), `build_batch(10)`, `stub()`. Run on factory_boy 3.3.3 with Django (in-memory SQLite): `OrderFactory(refunded=True)` gave status `refunded`, total 0 and saved one order plus one user via the SubFactory; `OrderFactory.build()` left `pk` None and created no user (the SubFactory follows the build strategy); `build_batch(10)` and `stub()` worked.
- SQLAlchemy: `factory.alchemy.SQLAlchemyModelFactory` with `sqlalchemy_session` (and `sqlalchemy_session_persistence = "commit"` to save the row; ran with an in-memory engine).

## TypeScript: Fishery
```ts
import { Factory } from 'fishery';
export const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence, email: `user${sequence}@example.test`, role: 'member',
}));
const admin = userFactory.build({ role: 'admin' });
```
(Ran on fishery 2.4.0: `sequence` started at 1 and increments per `build`.)

## Java: builder
```java
Order order = anOrder().withStatus(REFUNDED).build();   // aNew().with...() pattern, defaults in the builder
```

## Rules
- Defaults must be valid and minimal; no randomness that changes behaviour (random enum values cause flakes).
- Unique fields use sequences, not Faker, to avoid collisions.
- One factory per aggregate; traits for common variants instead of many factories.
- Keep factories next to tests, not in production code.

## Gotchas
- Deep SubFactory chains create many rows per test and slow suites; use `build` where persistence is not needed.
- Shared mutable defaults (lists/dicts) leak between tests: a class attribute `tags = []` on a factory gave the second object the first object's appended value (`[1]`), while `factory.LazyFunction(list)` gave a fresh `[]` each time.

## Verify
Tests read with only relevant attributes set, factories produce valid objects alone (`UserFactory()` passes model validation), and suite time stays flat.
