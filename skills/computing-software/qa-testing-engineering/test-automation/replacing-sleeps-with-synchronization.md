---
id: computing-software.qa-testing-engineering.test-automation.replacing-sleeps-with-synchronization
name: replacing-sleeps-with-synchronization
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [hard-coded-sleeps, synchronization-waits, explicit-waits, flaky-tests, wait-for-condition]
level: practitioner
status: gated
description: "Remove hard-coded sleeps from automated tests by waiting on observable conditions: UI state, network responses, polling APIs with backoff, events and test hooks in the app."
sources:
  - https://playwright.dev/docs/actionability
  - https://www.selenium.dev/documentation/webdriver/waits/
  - https://docs.cypress.io/app/core-concepts/retry-ability
  - https://testing.googleblog.com/2008/04/tott-avoiding-flakey-tests.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing sleeps with synchronization

Sleeps are both slow (always wait the maximum) and flaky (sometimes not long enough). Replace each with a wait for the condition the sleep was hoping for.

## Find them
```bash
grep -rnE "sleep\(|waitForTimeout|cy\.wait\([0-9]|Thread\.sleep|time\.sleep" tests/
```

## Replacement table
| Sleep was waiting for | Wait on instead |
|---|---|
| element to appear/enable | Playwright `await expect(loc).toBeVisible()/toBeEnabled()`; Selenium `WebDriverWait(...).until(EC.element_to_be_clickable(...))`; Cypress `cy.get(sel).should('be.enabled')` |
| spinner to go away | `await expect(spinner).toBeHidden()` / `EC.invisibility_of_element_located` |
| XHR to finish | `page.waitForResponse(...)` started before the action; `cy.intercept(...).as('x'); cy.wait('@x')` |
| background job to complete | poll an API with timeout and backoff (below) |
| animation | disable animations in test builds (`prefers-reduced-motion`, CSS override) |
| message on a queue | consume with a timeout; or a test hook endpoint that reports processing done |
| eventual consistency (search index) | poll the read side until the item appears, bounded |

Run checks: the `grep` pattern flagged `time.sleep`, `waitForTimeout`, `Thread.sleep` and a numeric `cy.wait(500)` (even inside a comment) but not `cy.wait("@x")`; Playwright 1.64.1 on Chromium ran a test with `toBeEnabled`, `toBeHidden`, `waitForResponse` started before the click and `toHaveText` against a page with a 500 ms enable delay and a delayed fetch, and passed; Selenium has `EC.element_to_be_clickable` and `EC.invisibility_of_element_located`; the Cypress docs list `cy.intercept(...).as()` with `cy.wait()` and the `be.enabled` assertion.

## Polling helper (Python)
```python
def wait_until(fn, timeout=30, interval=0.2, backoff=1.5, max_interval=2):
    deadline = time.monotonic() + timeout
    while True:
        result = fn()
        if result:
            return result
        if time.monotonic() > deadline:
            raise TimeoutError(f"condition not met in {timeout}s")
        time.sleep(interval)
        interval = min(interval * backoff, max_interval)
```
The helper ran: it returned after about 1 s when the condition turned true and raised `TimeoutError: condition not met in 1s` otherwise. Playwright: `expect.poll(fn).toBeGreaterThan(2)` and `expect(async () => ...).toPass()` both retried until the third attempt in a run. Awaitility in Java (`await().atMost(30, SECONDS).until(...)`; the Awaitility README shows the `Duration.ofSeconds(5)` form) was not compiled (gated: unconfirmed, source is paywalled or blocked); reason: no Java build tooling here.

## App-side testability
Expose readiness signals: `data-loading="false"` attributes, a `window.__appIdle` flag, or an `/test/jobs/{id}` status endpoint in test environments. Cheap for developers, removes guesswork for tests.

## Gotchas
- A wait on the wrong condition (element exists but data not loaded) is still a race: wait for the content, not the container.
- Very long timeouts mask performance regressions; keep them at hang-detection level.

## Verify
Suite runtime drops and the formerly flaky tests pass `--repeat-each=50` without retries.
