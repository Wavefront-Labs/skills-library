---
id: computing-software.data-engineering.etl-pipeline-design.test-data-and-synthetic-fixtures
name: test-data-and-synthetic-fixtures
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, pipeline-testing, test-data-generation, synthetic-data, fixtures, faker, hypothesis, data-masking, edge-cases]
level: practitioner
status: draft
description: "Build test data for pipelines: hand-written edge-case fixtures, Faker-generated volume data, property-based tests with Hypothesis, and masked production subsets."
sources:
  - https://faker.readthedocs.io/en/master/
  - https://hypothesis.readthedocs.io/en/latest/
  - https://docs.getdbt.com/docs/build/unit-tests
  - https://sdv.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test data and fixtures for pipelines

**Goal:** tests that exercise the cases that break pipelines in production, using data that is small, deterministic, and contains no real personal data.

## 1. Three kinds of test data
| Kind | Use for | Size |
|---|---|---|
| Hand-written fixtures | unit tests of a transform, exact expected output | 3-30 rows |
| Generated (Faker / SDV) | volume, performance, demo environments | thousands-millions |
| Masked prod subset | realistic distributions, integration tests | sampled |

## 2. Hand-written fixtures: the edge-case checklist
Write one row for each of:
- NULL in every nullable column; empty string vs NULL.
- Duplicate business key (same key, two `updated_at`s; same key, identical timestamps).
- Late/out-of-order record; record dated in the future; DST boundary timestamps; leap day.
- Unicode (accents, emoji, RTL), leading/trailing whitespace, very long strings.
- Zero, negative, max-precision decimals; currency with 0 and 3 decimal places.
- Orphan foreign key (fact with no dimension row).
- Deleted record / tombstone if the source supports deletes.

Keep fixtures as CSV/YAML next to the test; dbt unit tests take `given`/`expect` rows inline.

## 3. Generated data with Faker
```python
from faker import Faker
import random, csv
Faker.seed(42); random.seed(42)           # deterministic across runs
fake = Faker(["en_GB", "de_DE"])
with open("orders.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order_id", "customer_email", "amount", "created_at"])
    for i in range(100_000):
        w.writerow([i, fake.email(), round(random.lognormvariate(3, 1), 2),
                    fake.date_time_between("-1y", "now").isoformat()])
```
Model the skew you see in prod (lognormal amounts, a few hot customers) — uniform data hides skew and join-explosion bugs. For multi-table realism with preserved correlations, SDV synthesizers learn from a sample.

## 4. Property-based tests (Hypothesis)
```python
from hypothesis import given, strategies as st
@given(st.lists(st.tuples(st.integers(0, 50), st.integers(0, 10**6)), max_size=200))
def test_dedupe_keeps_latest(rows):
    out = dedupe_latest(rows)                       # (key, ts) pairs
    assert len({k for k, _ in out}) == len(out)     # unique keys
    assert all(ts == max(t for k2, t in rows if k2 == k) for k, ts in out)
```
Hypothesis shrinks failures to the minimal counterexample — ideal for dedupe, merge and window logic.

## 5. Masked prod subsets
- Subset by entity (pick 1% of customers, then all their orders) so foreign keys stay consistent.
- Mask deterministically (`sha2(email || salt)`) so joins on masked keys still work; never ship the salt to the test environment.
- Treat even masked subsets as sensitive if quasi-identifiers (DOB + postcode) remain.

## Verify
- [ ] Re-running the generator gives byte-identical output (seeded).
- [ ] Every item on the edge-case checklist has a fixture row or a reason it cannot occur.
- [ ] No test dataset contains real emails, names or IDs (scan with the PII classifier).
