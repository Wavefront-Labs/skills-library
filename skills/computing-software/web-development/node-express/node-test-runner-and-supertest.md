---
id: computing-software.web-development.node-express.node-test-runner-and-supertest
name: node-test-runner-and-supertest
category: computing-software
field: web-development
product: node-express
tags: [node, node-test-runner, supertest, node-test, mocking, coverage, api-testing, web-development]
level: practitioner
status: verified
description: "Testing Node/Express apps with the built-in node:test runner and supertest: test structure, mocks and fake timers, coverage, watch mode and test databases."
sources:
  - https://nodejs.org/api/test.html
  - https://github.com/ladjs/supertest
  - https://nodejs.org/en/learn/test-runner/using-test-runner
  - https://nodejs.org/api/test.html#mocking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node:test and supertest

**Goal:** dependency-light tests for services and HTTP endpoints using Node's built-in runner.

## 1. Export the app, listen elsewhere
```js
// app.js
export const app = express();  /* routes */
// server.js
import { app } from "./app.js"; app.listen(process.env.PORT);
```
Supertest binds the app to an ephemeral port per request; no real port needed.

## 2. An HTTP test
```js
// test/orders.test.js
import { test, describe, before, after } from "node:test";
import assert from "node:assert/strict";
import request from "supertest";
import { app } from "../app.js";

describe("POST /orders", () => {
  test("creates an order", async () => {
    const res = await request(app).post("/orders")
      .set("Authorization", `Bearer ${token}`)
      .send({ sku: "A1", qty: 2 })
      .expect("Content-Type", /json/)
      .expect(201);
    assert.equal(res.body.qty, 2);
  });
  test("rejects bad input", async () => {
    await request(app).post("/orders").send({ qty: -1 }).expect(400);
  });
});
```

## 3. Running
```bash
node --test                                   # finds **/*.test.{js,mjs,cjs}, test/**, etc.
node --test --watch
node --test --experimental-test-coverage --test-reporter=spec
node --test --test-name-pattern="rejects"
node --env-file=.env.test --test
```
Each file runs in its own process by default (isolation; three test files printed three different PIDs); use `--test-concurrency` to tune.

## 4. Mocks and timers
```js
test("retries", async (t) => {
  const send = t.mock.fn(async () => { throw new Error("down"); });
  t.mock.method(mailer, "send", send);
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const p = notify(user);
  for (let i = 0; i < 3; i++) { await new Promise((r) => setImmediate(r)); t.mock.timers.tick(5000); }   // one tick per pending retry delay
  await p.catch(() => {});
  assert.equal(send.mock.callCount(), 3);
});
```
Mocks created via `t.mock` reset automatically after the test. Module mocking: `t.mock.module()` (experimental, `--experimental-test-module-mocks`).

## 5. Databases
Use a real database in a container (Testcontainers or docker compose) with migrations run in `before`, and transactions rolled back or tables truncated between tests. Mocking the ORM hides real query bugs.

## 6. TypeScript
Node 22.18+/23.6+ strips types natively (`node --test "**/*.test.ts"`); otherwise `node --import tsx --test`.

## Verify
- [ ] `node --test` passes in CI with coverage report.
- [ ] Every endpoint has at least a happy path and an auth/validation failure test.
- [ ] Tests run in random order without interference (no shared mutable state).
