---
id: computing-software.qa-testing-engineering.cypress.timeouts-and-retry-tuning
name: timeouts-and-retry-tuning
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [defaultcommandtimeout, cypress-timeouts, pageloadtimeout, requesttimeout, retry-ability]
level: practitioner
status: verified
description: "Tune Cypress timeouts (defaultCommandTimeout, pageLoadTimeout, requestTimeout, responseTimeout, taskTimeout) globally and per command without masking slowness."
sources:
  - https://docs.cypress.io/app/references/configuration#Timeouts
  - https://docs.cypress.io/app/core-concepts/retry-ability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts and retry tuning

| Option | Default | Applies to |
|---|---|---|
| `defaultCommandTimeout` | 4000 | DOM queries and assertions (get, find, should) |
| `pageLoadTimeout` | 60000 | `cy.visit`, page transitions |
| `requestTimeout` | 5000 | `cy.wait('@alias')` waiting for the request to go out |
| `responseTimeout` | 30000 | `cy.wait` for the response, `cy.request` |
| `taskTimeout` | 60000 | `cy.task` (per call: `cy.task(name, arg, { timeout })`; a 500 ms override timed out a 3 s task) |

`execTimeout` and `cy.exec` were removed in Cypress 16.0.0 (use `cy.task`). Defaults above were read from `Cypress.config()` on 16.2.0.

```js
// cypress.config.js
module.exports = defineConfig({ e2e: { defaultCommandTimeout: 6000 } });
// per command
cy.get('[data-cy=report]', { timeout: 30000 }).should('be.visible');
cy.wait('@export', { responseTimeout: 120000 });
// per test / suite
it('slow export', { defaultCommandTimeout: 20000 }, () => { ... });
Cypress.config('defaultCommandTimeout', 10000);   // persisted into the following tests of the spec in a 16.2.0 run
```

## What retries
Queries + the assertions chained after them retry as a unit. Actions (`click`, `type`) do not retry; if they fail actionability they wait up to the timeout, then fail.

## Tune, don't inflate
- Raise timeouts only on known-slow steps; a global 30s timeout makes every real failure take 30s.
- If a query needs >4s routinely, find a better readiness signal (`cy.wait('@loadData')`, loading spinner gone).

## Gotchas
- A `{ timeout }` on a query applies to that query and the assertions chained to it; give each query that needs longer its own `{ timeout }`. `{ timeout: 0 }` disables retrying (retry-ability docs).
- Per-test overrides work (`it('slow', { defaultCommandTimeout: 20000 }, ...)` reported 20000).
- `Cypress.config('viewportWidth', ...)` during a test throws since 16.0.0; use `cy.viewport()` or test config.
- `cy.wait(5000)` (number) is a hard sleep, not a timeout; avoid.

## Verify
Run on Cypress 16.2.0 (defaults, per-test override, runtime change, task timeout). `grep -r "cy.wait([0-9]"` returns nothing; slow-step timeouts are local and commented.
