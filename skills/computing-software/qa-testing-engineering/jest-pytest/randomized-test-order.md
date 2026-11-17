---
id: computing-software.qa-testing-engineering.jest-pytest.randomized-test-order
name: randomized-test-order
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-randomly, random-test-order, test-order-dependence, flaky-tests, jest-randomize]
level: practitioner
status: verified
description: "Run tests in random order to expose hidden dependence: pytest-randomly seeds, Jest --randomize, JUnit 5 MethodOrderer.Random, RSpec --order rand, and replaying a failing seed."
sources:
  - https://github.com/pytest-dev/pytest-randomly
  - https://jestjs.io/docs/cli#--randomize
  - https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-execution-order
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Randomised test order

**Goal:** make order-dependent tests fail early and reproducibly, instead of mysteriously when someone adds a test.

## pytest
```bash
pip install pytest-randomly        # active once installed: shuffles modules, classes, tests
pytest                              # header prints: Using --randomly-seed=1553614239 (not shown with -q)
pytest -p randomly --randomly-seed=1553614239   # replay the exact order
pytest --randomly-seed=last         # reuse previous seed
pytest -p no:randomly               # disable for debugging
```
It also reseeds `random`, Faker, factory_boy and NumPy's legacy random state (`np.random.*`, not `default_rng`) per test, so random data is reproducible with the seed (checked: same seed gave identical `random`, NumPy and Faker values).
Alternative: `pytest-random-order`, which is opt-in (nothing shuffles until you pass a flag); `--random-order-bucket` takes global, package, module, class, parent, grandparent or none.

## Jest
```bash
npx jest --randomize            # shuffles tests within a file; the seed is printed in the summary (Jest 30)
npx jest --randomize --seed=1234
```
Files already run in parallel workers in nondeterministic order.

## JUnit 5
```properties
# src/test/resources/junit-platform.properties
junit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random
junit.jupiter.testclass.order.default=org.junit.jupiter.api.ClassOrderer$Random
junit.jupiter.execution.order.random.seed=42
```
The seed is logged at CONFIG level when not set. Property names confirmed in the JUnit javadoc (`MethodOrderer.Random`, `ClassOrderer.Random`); the JUnit and RSpec commands were not executed here (no JDK or Ruby).

## Others
RSpec `--order rand` / `--seed 1234`; Go `go test -shuffle=on` (prints `-test.shuffle` seed);

## Workflow when a seed fails
1. Rerun with the seed to confirm.
2. Find the polluter: bisect the test list run before the victim (`detect-test-pollution` for pytest, a PyPI package; not run here).
3. Fix isolation (fixture scope, global state, DB reset); add a regression by running the pair in both orders.

## Gotchas
- Always print and store the seed in CI logs; without it the failure is lost.
- Some suites intentionally order (integration flows); mark them explicitly rather than disabling randomisation globally.

## Verify
CI runs with random order on every build, seeds appear in logs, and a known failing seed can be replayed locally.
