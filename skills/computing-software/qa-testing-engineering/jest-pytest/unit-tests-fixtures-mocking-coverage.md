---
id: computing-software.qa-testing-engineering.jest-pytest.unit-tests-fixtures-mocking-coverage
name: unit-tests-fixtures-mocking-coverage
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, jest, junit, junit5, vitest, unit-testing, integration-testing, assertions, fixtures, conftest, parametrize, mocking, monkeypatch, unittest-mock, jest-mock, mockito, test-doubles, coverage, pytest-cov, coverage-py, istanbul, jacoco, branch-coverage, tmp-path, python, javascript, typescript, java, tdd]
level: practitioner
status: gated
description: "Unit and integration tests in pytest, Jest and JUnit 5: arrange-act-assert, fixtures and parametrization, mocking at the right boundary (patch where looked up), and branch coverage gates."
sources: ["https://docs.pytest.org/en/stable/", "https://jestjs.io/docs/getting-started", "https://junit.org/junit5/docs/current/user-guide/", "https://coverage.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit tests that catch bugs: pytest, Jest, JUnit 5

**Goal:** fast, isolated tests that fail for one reason, with fixtures for setup,
mocks only at real boundaries, and coverage used as a gap-finder rather than a target.

## 1. Shape of a good test
Arrange, act, assert; one behaviour per test; name it after the behaviour:
`test_refund_rejected_after_30_days`. A test should fail if — and only if — that
behaviour breaks. Assert on outputs and observable effects, not private internals.

## 2. pytest
```python
# test_pricing.py
import pytest
from shop.pricing import apply_discount

@pytest.mark.parametrize("total, code, expected", [
    (100, "TEN", 90),
    (100, None, 100),
    (5, "TEN", 4.5),
])
def test_apply_discount(total, code, expected):
    assert apply_discount(total, code) == pytest.approx(expected)   # approx for floats

def test_unknown_code_raises():
    with pytest.raises(ValueError, match="unknown code"):
        apply_discount(100, "BOGUS")
```
**Fixtures** (put shared ones in `conftest.py`; pytest finds them automatically):
```python
@pytest.fixture
def repo(tmp_path):                     # tmp_path: built-in, unique dir per test
    r = Repo(tmp_path / "db.sqlite"); r.migrate()
    yield r                             # code after yield = teardown, runs even on failure
    r.close()
```
Scope (`scope="session"`) only for expensive, read-only resources; shared mutable
state across tests causes order-dependent failures.
Run: `pytest -q -x --lf` (stop at first failure, rerun last failures), `-k refund` to filter. The pytest examples in this section were run (10 tests pass; `--cov-branch --cov-fail-under` works and reports branch data).

## 3. Jest (Vitest is API-compatible for most of this)
```js
import { applyDiscount } from './pricing'
test.each([[100, 'TEN', 90], [100, null, 100]])('discount %p %p -> %p', (t, c, e) => {
  expect(applyDiscount(t, c)).toBeCloseTo(e)
})
test('rejects unknown code', () => {
  expect(() => applyDiscount(100, 'BOGUS')).toThrow(/unknown code/)
})
test('loads user', async () => {
  await expect(loadUser(1)).resolves.toMatchObject({ id: 1 })   // always await/return async assertions
})
```
`toBe` is identity (`Object.is`); use `toEqual`/`toStrictEqual` for objects. A
forgotten `await` on an async assertion lets the test finish before the assertion settles: in a Jest 30 / Node 20 run the failure surfaced on the wrong test or as a crashed worker, so do not rely on it failing cleanly.

## 4. JUnit 5 (gated: unconfirmed, source is paywalled or blocked)
No JDK was available, so these Java snippets were not compiled or run.
```java
@ParameterizedTest
@CsvSource({"100,TEN,90", "100,,100"})
void appliesDiscount(double total, String code, double expected) {
    assertEquals(expected, Pricing.apply(total, code), 0.001);
}
@Test void rejectsUnknownCode() {
    var ex = assertThrows(IllegalArgumentException.class, () -> Pricing.apply(100, "BOGUS"));
    assertTrue(ex.getMessage().contains("unknown code"));
}
```
`@BeforeEach`/`@AfterEach` for per-test setup; Mockito (`@ExtendWith(MockitoExtension.class)`,
`@Mock`, `when(...).thenReturn(...)`, `verify(...)`) for doubles.

## 5. Mocking: where and how much
- Mock **boundaries you don't own or that are slow/non-deterministic**: HTTP, clock,
  randomness, email, payment gateways. Don't mock your own pure logic or the code under test.
- **Python: patch where the name is looked up, not where it's defined.** If
  `shop/orders.py` does `from shop.mail import send`, patch `shop.orders.send`, not
  `shop.mail.send`. This is the #1 "my mock isn't applied" bug.
```python
from unittest.mock import patch
def test_order_sends_receipt():
    with patch("shop.orders.send", autospec=True) as send:   # autospec: wrong signature fails
        place_order(...)
    send.assert_called_once()
```
  pytest's `monkeypatch.setattr(...)` / `monkeypatch.setenv(...)` auto-undo after the test.
- Jest: `jest.mock('./mail')` is hoisted above imports; reset between tests with
  `clearMocks: true` in config (or `jest.clearAllMocks()` in `afterEach`). `restoreMocks: true` alone did not reset call counts of an automocked function in Jest 30 (run), it only restores spies.
- Freeze time instead of sleeping: Jest `jest.useFakeTimers()`; Python `freezegun` (gated: unconfirmed, source is paywalled or blocked) or
  inject a clock.
- Too many mocks in one test = design smell; the test now verifies wiring, not behaviour.

## 6. Coverage
```bash
pytest --cov=shop --cov-branch --cov-report=term-missing --cov-fail-under=80
npx jest --coverage        # istanbul; set coverageThreshold in jest.config
mvn verify                 # with the jacoco-maven-plugin check goal configured (gated: unconfirmed, source is paywalled or blocked)
```
Turn on **branch** coverage — line coverage counts an `if` as covered when only one
side ran. Read the `Missing` column for untested branches in risky code; don't write
assertion-free tests to move the number.

## Unconfirmed / notes
The pytest and Jest snippets were run (pytest 9.1, pytest-cov 7.1, Jest 30); the Java, Mockito, mvn/JaCoCo and freezegun parts were not. Check pytest-cov flag names and Jest config
keys against your installed versions. The 80% threshold is an example, not a rule.

## Verify
- [ ] Each test fails when you break the behaviour it names (mutate the code once to check).
- [ ] Suite passes in random order (`pytest -p randomly` / `jest --randomize`).
- [ ] No real network, clock or filesystem outside `tmp_path`/temp dirs in unit tests.
- [ ] Patches target the importing module; `autospec`/typed mocks used.
- [ ] Branch coverage reported in CI with a failing threshold.
