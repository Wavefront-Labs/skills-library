---
id: computing-software.web-development.rails.testing-with-rspec-and-factories
name: testing-with-rspec-and-factories
category: computing-software
field: web-development
product: rails
tags: [rails, rspec, factory_bot, fixtures, request-spec, system-spec, capybara, test-suite-speed, ruby, web-development]
level: advanced
status: draft
description: "Rails testing with RSpec: FactoryBot vs fixtures tradeoffs, request vs system specs, and the usual causes of a slow or flaky suite."
sources:
  - https://rspec.info/
  - https://github.com/thoughtbot/factory_bot
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rails testing with RSpec — specs that stay fast and reliable

**Goal:** a suite where a failure means the code broke, not "flaky again," and
where adding tests doesn't quietly make CI slower every sprint.

## 1. FactoryBot vs fixtures — this is a real tradeoff, not just taste
- **Fixtures**: loaded once per suite run (fast), but shared global state
  across all tests — a test that mutates a fixture row can bleed into another
  test's expectations depending on run order, and fixture YAML drifts from
  model validations silently (no validation runs on fixture load by default).
- **FactoryBot**: builds exactly the object graph each test needs, validations
  run normally, no shared state — but creates fresh DB rows per test, which
  adds up in a large suite if overused (`create` triggers a real INSERT;
  `build`/`build_stubbed` don't).
Default to `build_stubbed` (no DB hit, unsaved object with a fake id) for unit
tests that don't need persistence; reserve `create` for request/system specs
that exercise real persistence/associations, or unit tests that specifically
need DB-level behavior (a uniqueness validation, a DB constraint).

## 2. Request specs vs system specs — pick by what's actually under test
- **Request spec**: exercises the full stack through the router down to the
  response, without a browser — fast, good default for testing a controller's
  behavior (status codes, JSON shape, redirects, auth gating).
- **System spec** (Capybara + a real or headless browser driver): the only
  kind that runs actual JS, so it's the right (and only) choice for testing
  Stimulus/Turbo interactivity or a JS-dependent flow — but an order of
  magnitude slower per test and the most common source of suite flakiness.
Don't write a system spec to test something a request spec could cover just
because it "feels more end-to-end" — that trade is rarely worth the speed and
flakiness cost for logic with no real client-side behavior involved.

## 3. The usual causes of flaky system specs
- **Missing explicit waits**: asserting on an element immediately after a
  click that triggers an async JS update — Capybara's matchers (`have_content`,
  `have_selector`) already retry/wait up to a timeout by default, but a raw
  `page.find(...).text == 'x'` comparison does not; use the waiting matcher
  form, not a manual string comparison.
- **Database cleaner strategy mismatch**: `transaction` strategy (fast,
  wraps each test in a rollback) doesn't work across separate processes
  (the test process and a headless-browser-driven server process see
  different uncommitted transactions) — system specs typically need the
  `truncation` or `deletion` strategy, which is slower; mixing strategies
  incorrectly is a common cause of "data from a previous test is still there"
  flakiness specific to system specs.
- **Shared, mutated global state** (Rails cache, a class-level memoized
  value) not reset between tests — add explicit teardown (`Rails.cache.clear`
  in an `after` hook) rather than discovering order-dependent failures.

## 4. Suite speed — the big levers
- **Parallel testing** (`parallel_tests` gem or Rails' built-in
  `parallelize`) splits the suite across multiple DB-backed processes — the
  single highest-leverage speed fix for a large suite, but needs each process
  to get its own DB (via `parallelize_setup`), or tests collide on data.
- **`build_stubbed` over `create`** wherever persistence isn't actually needed
  (see above) — cuts DB round trips dramatically across a large unit-test
  suite.
- **Avoid `before(:each)` doing expensive setup used by only some examples in
  the block** — scope expensive factory creation to the specific `context`
  that needs it rather than a blanket outer `before`.
- **`--only-failures`/`--next-failure` (rspec flags)** during active debugging
  to avoid re-running the whole suite per iteration.

## Verify
- [ ] Unit specs default to `build_stubbed`; `create` is reserved for tests that need real persistence/associations.
- [ ] System specs exist only for genuinely JS-dependent behavior; everything else is a request spec.
- [ ] Capybara assertions use the waiting matcher form (`have_content`), not a raw synchronous read-and-compare.
- [ ] Database cleaner strategy matches spec type (transactional for unit/request, truncation/deletion for system specs across processes).
- [ ] The suite runs in parallel in CI, with each worker on its own test database.
