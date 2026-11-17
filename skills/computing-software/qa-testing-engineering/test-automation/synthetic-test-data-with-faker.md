---
id: computing-software.qa-testing-engineering.test-automation.synthetic-test-data-with-faker
name: synthetic-test-data-with-faker
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [synthetic-test-data, faker, test-data-management, data-generation, seeded-data]
level: practitioner
status: verified
description: "Generate realistic synthetic test data with Faker (Python and JS): locales, seeding for reproducibility, uniqueness, bulk volumes and privacy-safe datasets."
sources:
  - https://faker.readthedocs.io/en/master/
  - https://fakerjs.dev/guide/
  - https://www.istqb.org/certifications/test-analyst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic test data with Faker

**Goal:** realistic, privacy-safe data in any volume, reproducible on demand.

## Python
```python
from faker import Faker
Faker.seed(1234)                       # reproducible across runs
fake = Faker(["en_GB", "de_DE", "ja_JP"])
row = {
    "name": fake.name(),
    "email": fake.unique.email(),       # unique proxy; fake.unique.clear() between datasets
    "iban": fake.iban(),
    "dob": fake.date_of_birth(minimum_age=18, maximum_age=90),
    "address": fake.address(),
}
```
pytest plugin: the `faker` fixture is re-seeded for every test with the same seed (two tests drawing `faker.name()` get the same value), so values repeat across tests; override the seed with a `faker_seed` fixture (checked on Faker 40.43).

## JavaScript
```js
import { faker, fakerDE } from '@faker-js/faker';
faker.seed(1234);
const users = faker.helpers.multiple(() => ({
  id: faker.string.uuid(), name: faker.person.fullName(), email: faker.internet.email(),
}), { count: 1000 });
```

## Bulk volumes
- Generate to CSV/JSON once and load via `COPY`/bulk insert; generating millions of rows inside tests is slow.
- Postgres alternative for volume: `generate_series` with `md5(random()::text)`.
- Keep referential integrity: generate parents first, sample their ids for children.

## Make it realistic
- Locales exercise i18n (umlauts, kanji, long names).
- Skewed distributions matter for performance tests: real data is Zipf-like, not uniform (few customers with many orders).
- Add edge cases deliberately (empty optional fields, max lengths); Faker values are "typical", not boundary.

## Gotchas
- Faker values can be invalid for your rules (phone formats, postcodes); validate generated data against the same rules as the app.
- Unseeded random data makes failures non-reproducible; always log the seed.
- Python `fake.email()` is already safe by default (`safe=True` gives example.com/org/net), but `fake.free_email()` and `fake.email(safe=False)` return real providers (yahoo.com, hotmail.com). In JS `faker.internet.email()` returns real providers (gmail, yahoo, hotmail in a run on @faker-js/faker 10.6); use `faker.internet.exampleEmail()` or `faker.internet.email({ provider: 'example.test' })`.
- The `iban` provider is not locale specific here: `Faker(["en_GB","de_DE","ja_JP"]).iban()` returned both a DE and a GB number across calls, so a multi-locale proxy picks a locale per call; use one locale per dataset if the country matters.

## Verify
Same seed reproduces identical data, generated rows pass application validation, and no real personal data is present.
