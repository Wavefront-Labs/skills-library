---
id: computing-software.qa-testing-engineering.test-case-design.regression-pack-automation-and-scheduling
name: regression-pack-automation-and-scheduling
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [regression-pack, nightly-regression, regression-testing, test-types, ci-scheduling]
level: practitioner
status: verified
description: "Build, tier and schedule the automated regression pack: PR, merge, nightly and pre-release suites, with runtime budgets, ownership and pruning."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule
  - https://docs.pytest.org/en/stable/example/markers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automating and scheduling the regression pack

**Goal:** catch regressions fast without running everything on every commit. CTFL v4.0 section 2.2.3 says regression suites are run many times, grow with each release, and are strong candidates for automation.

## Tiers
| Suite | Trigger | Budget | Content |
|---|---|---|---|
| PR / pre-merge | every push | < 10 min | unit, component, contract, critical API checks, affected-tests selection |
| Post-merge | main branch | < 30 min | full API, key E2E journeys |
| Nightly | cron | 1-3 h | full E2E, cross-browser, slower integration, visual |
| Pre-release | release candidate | as needed | everything + non-functional smoke + manual risk-based checks |

## Tagging
```python
@pytest.mark.regression_nightly
def test_invoice_pdf_layout(): ...
```
`pytest -m "not regression_nightly"` on PRs, `-m regression_nightly` at night (both run). Register the marker (`markers =` in `pytest.ini`) or pytest warns; with `--strict-markers` an unregistered marker is a collection error. Playwright: `--grep @nightly`; JUnit 5: `@Tag("nightly")` with Surefire `groups`.

## Scheduling (GitHub Actions)
```yaml
on:
  schedule:
    - cron: "0 2 * * 1-5"   # 02:00 UTC weekdays
  workflow_dispatch: {}
```
Post results to the team channel; a red nightly is triaged first thing by a rota owner.

## Maintaining the pack
- Each test has an owner and a linked requirement/risk; untraced tests are candidates for deletion.
- Quarterly prune: remove duplicates, move combinatorial E2E cases down to unit level, retire tests for removed features.
- Track runtime trend and flake rate per suite; quarantine flaky tests with a ticket and an expiry.

## Gotchas
- A nightly that is red for a week is ignored; treat it as a stop-the-line event or delete the failing tests.
- Nightly-only tests find bugs a day late; promote high-value ones to post-merge as they get faster.
- Scheduled workflows on GitHub run on the default branch only (the file must exist there), may be delayed under load (the start of every hour is busy, so avoid minute 0; queued jobs may be dropped), and in a public repository are disabled after 60 days without repository activity (GitHub docs, events that trigger workflows).

## Verify
Every regression test belongs to exactly one tier, runtimes are within budget, and the last 10 nightly runs have an owner-acknowledged outcome.
