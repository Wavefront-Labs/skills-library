---
id: computing-software.qa-testing-engineering.jest-pytest.test-doubles-and-mocking-boundaries
name: test-doubles-and-mocking-boundaries
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [mocking, test-doubles, stubs, spies, fakes, mocks, dummies, london-school, classical-tdd, mockist, state-based-testing, interaction-testing, over-mocking, unittest-mock, jest-mock, sinon, mockito, patch-where-looked-up, mock-patch, test-fragility, refactoring-resistance, pytest, jest]
level: advanced
status: verified
description: "Choose the right test double (dummy/stub/fake/spy/mock) and the right boundary to double at, so tests survive refactors instead of breaking on every internal change."
sources: ["Gerard Meszaros, xUnit Test Patterns (Addison-Wesley, 2007)", "Martin Fowler, 'Mocks Aren't Stubs' https://martinfowler.com/articles/mocksArentStubs.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Test doubles: picking the right one, and the right boundary

**Goal:** tests that catch real breakage and stay green through a refactor that
doesn't change behavior — the opposite of what most teams get when "mocking" means
one tool used for everything.

## 1. The five kinds, and when each is right
- **Dummy**: a value passed but never used (e.g., a null logger). No behavior.
- **Stub**: returns canned answers to calls made during the test; no assertions on
  how it was called. Use for *state-based* testing — "given this input, is the
  output right?"
- **Fake**: a working lightweight implementation (in-memory DB, in-memory queue).
  Use when the real dependency is slow/external but its *behavior* matters (e.g., a
  repository that must actually store-then-retrieve).
- **Spy**: a real or wrapped object that records calls so you can assert on them
  afterward, while still delegating to real behavior.
- **Mock**: pre-programmed with expectations on *how* it will be called
  (`expect(fn).toHaveBeenCalledWith(...)`); the test fails if the interaction
  pattern differs, even if the outcome is identical. Use only when the
  *interaction itself* is the behavior under test (e.g., "sending the email is
  what we're verifying," not just "the function returned 200").

## 2. Classical vs. London school — pick one default, not per-test
**Classical (state-based)**: double only true externals (network, filesystem,
clock, random); let real objects collaborate. Tests are fewer, more resistant to
refactors, but failures are less localized.
**London (mockist)**: double every collaborator, assert on interactions.
Pinpoints exactly which unit broke, but a pure internal refactor (renaming a
helper method, inlining a collaborator) breaks mock-based tests that never changed
observable behavior — the single biggest source of "the tests are more work than
the code" complaints. Default to classical for business logic; use London only at
true seams (a payment gateway call, a third-party API client).

## 3. Patch where it's *looked up*, not where it's *defined*
The #1 Python mocking bug: `unittest.mock.patch('mypkg.utils.send_email')` patches
the name in `mypkg.utils`, which does nothing if `mypkg.handlers` did
`from mypkg.utils import send_email` (it imported its own reference; reproduced: patching `shop.mail.send` left `place_order()` calling the real function, while patching `shop.orders.send` intercepted it). Patch
`mypkg.handlers.send_email` — the module under test's namespace. Jest's
`jest.mock('../utils')` patches the module registry so this gotcha doesn't apply
the same way, but the equivalent trap is mocking a named export that the caller
destructured at import time before the mock was registered — hoist `jest.mock`
calls (Jest's babel transform hoists top-level `jest.mock` calls: one placed after the `require` of the caller still took effect in a Jest 30 run; calls nested in functions or blocks are not hoisted).

## 4. Signs of over-mocking
- A test still passes after you delete the implementation and replace it with
  `return null` — it was testing the mock, not the code.
- More mock setup lines than assertion lines.
- A refactor that changes zero observable behavior breaks 10 tests — the tests are
  coupled to structure, not contract.
Fix: push the mock down to the real external boundary (HTTP client, DB driver,
clock) and let everything above it run for real in the test.

## 5. Fixtures and mocking together (pytest/Jest specifics)
In pytest, prefer `monkeypatch.setattr` for scoped, auto-reverting patches over
raw `unittest.mock.patch` context managers — it composes with fixtures and cleans
up even on test failure. In Jest, reset mock state between tests
(`jest.clearAllMocks()` in `afterEach`, or `clearMocks: true` in config; reproduced: with it off the second test saw a stale call count and failed) — a stale
call count from a previous test is a classic flaky-assertion source.

## Unconfirmed / notes
"Classical by default" is the Fowler/Meszaros consensus position, not a universal
rule — some teams run London school deliberately and successfully; state the
tradeoff when choosing, don't just default silently.

## Verify
- [ ] Each double is the weakest kind that proves the behavior (stub before mock).
- [ ] Mocks exist only at true externals, not between your own modules.
- [ ] Deleting the implementation and stubbing a wrong return makes the test fail.
- [ ] Python patches target the importing module's namespace, verified by running
      the test with the "wrong" patch target first to see it fail to patch.
- [ ] Mock state is reset between tests (`clearMocks`/`monkeypatch` scope).
