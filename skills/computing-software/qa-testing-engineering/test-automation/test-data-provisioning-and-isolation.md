---
id: computing-software.qa-testing-engineering.test-automation.test-data-provisioning-and-isolation
name: test-data-provisioning-and-isolation
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-data-provisioning, data-isolation, test-data-management, shared-environments, parallel-testing]
level: practitioner
status: docs-checked
description: "Provision isolated test data in shared environments: create-per-test via APIs, unique namespacing, data pools and reservation, cleanup and refresh."
sources:
  - https://martinfowler.com/articles/nonDeterminism.html
  - https://playwright.dev/docs/test-fixtures
  - https://playwright.dev/docs/api-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test data provisioning and isolation in shared environments

**Goal:** tests in SIT/staging (shared by teams and parallel runs) never fail because someone else changed or consumed their data.

## Why isolation
Martin Fowler's non-determinism article: keep tests isolated so one test cannot affect another; properly isolated tests can run in any order, which is what allows running subsets and parallelising. Lack of isolation is a common cause of non-determinism, databases being the usual culprit but static data and singletons (such as the logged-in user) too. If a teardown fails, the test can pass yet break later tests, so make teardown failures loud.

## Strategies (prefer top)
1. **Create per test, via API:** the test fixture creates the customer/order it needs through public or test-only APIs and deletes or abandons it afterwards. Fully isolated.
2. **Namespace per run:** prefix all created data with a run id plus a unique suffix, or create a tenant/organisation per pipeline run; queries in tests filter by namespace.
3. **Data pools with reservation:** for expensive data (aged accounts, verified users, third-party sandbox accounts), keep a pool and lease records with a lock table or a small reservation service; release on teardown, expire leases after a timeout.
4. **Read-only shared reference data:** product catalogue, countries, tax rates; never mutated by tests.

## Fixture example (Playwright)
Playwright fixtures establish the environment for each test and are isolated between tests; code after `await use(...)` is the teardown. The `request` fixture sends API requests. The endpoint below is a placeholder for your own test-only API.
```ts
import { randomUUID } from 'node:crypto';
export const test = base.extend<{ customer: Customer }>({
  customer: async ({ request }, use) => {
    const email = `qa-${randomUUID()}@example.test`;
    const res = await request.post("/test-api/customers", { data: { email, tier: "gold" } });
    const customer = await res.json();
    await use(customer);
    await request.delete(`/test-api/customers/${customer.id}`);
  },
});
```
pytest does the same with yield fixtures (see its fixtures how-to).

## Refresh and cleanup
- Scheduled cleanup job deletes namespaced test data older than an agreed age.
- Periodic environment refresh from a masked baseline; announce it, and make tests independent of pre-existing records.
- Track pool levels; alert when reservable accounts run low.

## Gotchas
- Tests that "find any existing order" collide in parallel; always create or lease.
- Test-only APIs must be disabled in production (deployment config check).
- Third-party sandboxes may have rate limits and shared state; check the vendor's terms, pool and throttle.

## Verify
The suite passes running twice in parallel against the same environment, and no test depends on records it did not create or lease.

## Checked
2026-11-09. Confirmed in Fowler's non-determinism article (isolation, parallelising, static data/singletons, loud teardown failures), the Playwright fixtures page (base.extend, use, isolation between tests) and the Playwright API testing page (request fixture, request.post with data). Removed: the "few hundred ms" figure, the run-id naming pattern as a fixed format, workerIndex/Date.now in the example, the pytest and third-party rate-limit specifics.
Method: documentation only; no commands were run.
