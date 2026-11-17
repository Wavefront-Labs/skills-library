---
id: computing-software.devops-ci-cd.ci-pipeline-design.property-based-testing-in-ci
name: property-based-testing-in-ci
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, property-based-testing, test-automation, fuzzing-in-ci]
level: advanced
status: docs-checked
description: "Run property-based tests (Hypothesis, fast-check, proptest) in CI with bounded examples, reproducible seeds, failure databases and longer nightly runs."
sources: ["https://hypothesis.readthedocs.io/en/latest/settings.html", "https://github.com/dubzzz/fast-check"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based testing in CI

Generate many inputs and check invariants (round-trip, idempotence, ordering, no-crash).

```python
from hypothesis import given, settings, strategies as st
@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)
```

## CI profiles
```python
# conftest.py
from hypothesis import settings, HealthCheck
settings.register_profile("ci", max_examples=200, deadline=None, derandomize=False,
                          print_blob=True, suppress_health_check=[HealthCheck.too_slow])
settings.register_profile("nightly", max_examples=5000)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))
```
- PRs: moderate examples to stay fast; nightly: many more.
- `print_blob=True` prints `@reproduce_failure(...)` so a CI failure replays locally.
- Persist Hypothesis's example database between CI runs (see its `database` setting).

## Other stacks
- fast-check (JS): failure output includes the seed and path; replay with them (see its docs).
- proptest (Rust): set `PROPTEST_CASES` to change the case count (default 256).

## Flakiness
Random generation can find a bug on one run and not the next. That is a real bug, not a flaky
test: capture the seed and add it as an explicit example (`@example(...)`).

## Verify
- [ ] An injected bug is found within the CI example budget and the failure prints a reproduction.

## Checked

2026-10-28. Confirmed against the Hypothesis settings reference: `settings.register_profile` / `load_profile`, `max_examples`, `deadline` (default None on CI), `derandomize`, `print_blob` (prints `@reproduce_failure`, default True on CI), `suppress_health_check` with `HealthCheck.too_slow`, the `database` setting; fast-check README (failure output shows seed and path); proptest config page (`PROPTEST_CASES`, default 256). Removed: `.hypothesis/` retry claim, fast-check `numRuns`, `proptest-regressions/` and the jqwik, FsCheck and rapid names.

Method: documentation only; no commands were run.
