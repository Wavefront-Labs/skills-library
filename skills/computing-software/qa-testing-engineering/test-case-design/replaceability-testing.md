---
id: computing-software.qa-testing-engineering.test-case-design.replaceability-testing
name: replaceability-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [replaceability-testing, portability-testing, component-replacement, vendor-swap, drop-in-replacement, istqb-tta]
level: practitioner
status: draft
description: "Test replaceability: a new component, library or vendor can replace the old one with equivalent behaviour, using shared contract tests and side-by-side comparisons."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replaceability testing

**Goal:** confirm a component can be swapped (DB engine, payment provider, library major version, OS) with no loss of required behaviour. CTAL-TTA v4.0 4.6.

## Approach
1. **Define the contract** the component fulfils: API surface, behaviour, performance, error semantics.
2. **Shared contract test suite** run against both implementations (parametrise the fixture):
   ```python
   @pytest.fixture(params=["postgres", "cockroach"])
   def repo(request): return make_repo(request.param)
   def test_save_and_load(repo): ...
   ```
3. **Differential testing**: same inputs to old and new, compare outputs (`differential-testing-reference`). For services, shadow traffic: mirror production requests to the new component and diff responses without serving them.
4. **Non-functional comparison**: performance benchmarks, resource use, failure behaviour.
5. **Migration of data and config** to the replacement (see `data-migration-testing`).

## Gotchas
- Subtle semantic differences: sorting/collation, null handling, rounding, timestamp precision, transaction isolation defaults.
- Error codes differ; callers may depend on specific ones.

## Verify
The contract suite passes on both, differential runs show no unexplained differences, and benchmarks are within agreed tolerance.
