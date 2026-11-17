---
id: computing-software.qa-testing-engineering.cypress.cy-task-node-side-work
name: cy-task-node-side-work
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-task, setupnodeevents, cypress-plugins, database-seeding, cypress-config]
level: practitioner
status: verified
description: "Run Node-side work from Cypress tests with cy.task: register tasks in setupNodeEvents for DB seeding, file system checks, email inboxes and logging, with return-value rules."
sources:
  - https://docs.cypress.io/api/commands/task
  - https://docs.cypress.io/api/node-events/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cy.task for Node-side work

**Goal:** do things the browser cannot (DB queries, file system, external services, console logging) from inside tests.

## Register tasks
```js
// cypress.config.js
const { defineConfig } = require('cypress');
// Example store: Node's built-in SQLite (Node 22+). Use your real driver (pg, mysql2, ...) the same way.
const { DatabaseSync } = require('node:sqlite');
const db = new DatabaseSync(':memory:');
db.exec('CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT)');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      on('task', {
        async 'db:seed'(scenario) {
          db.exec('DELETE FROM orders');
          if (scenario === 'basket-with-two-items') db.prepare('INSERT INTO orders (id, status) VALUES (?, ?)').run(42, 'PAID');
          return null;                                  // must return something other than undefined
        },
        async 'db:orderStatus'(id) {
          const row = db.prepare('SELECT status FROM orders WHERE id = ?').get(id);
          return row?.status ?? null;
        },
        log(message) { console.log(message); return null; },
      });
      return config;
    },
  },
});
```

## Use
```js
beforeEach(() => cy.task('db:seed', 'basket-with-two-items'));
cy.task('db:orderStatus', 42).should('eq', 'PAID');        // the task runs once and is not retried
cy.task('log', `seed done for ${Cypress.spec.name}`);
```
For polling, wrap in a recursive function or use `cypress-recurse`.

## Rules
- Return a value or a promise; returning `undefined` fails the test ("return null if you don't need a value").
- Arguments and results must be JSON-serialisable (a returned `Date` arrived as an ISO string and a function property was dropped).
- Default `taskTimeout` 60 s; override per call: `cy.task('db:seed', s, { timeout: 120000 })`.
- Tasks run in the Node process with the config's env, not in the browser.

## Common tasks
DB seed/reset, read test emails (Mailpit/MailHog API), generate files, read downloads directory, call internal admin APIs with secrets kept out of the browser.

## Gotchas
- `cy.task` is not retried like queries; `.should` after it does not re-run the task.
- Long-lived connections or handles (pools, the DB above): create them once at config load, not per task call.
- In component testing, register tasks under `component.setupNodeEvents` too (a task registered there ran from a component spec).

## Verify
Run on Cypress 16.2.0 (the seed and status tasks above, a task returning `undefined` failing with "returned undefined", a 500 ms per-call timeout, `taskTimeout` default 60000, and a failed `.should` not re-running the task: a later call returned 2). Seeding via task makes each spec independent of run order, and task failures surface the Node error in the command log.
