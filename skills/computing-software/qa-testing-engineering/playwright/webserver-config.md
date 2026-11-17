---
id: computing-software.qa-testing-engineering.playwright.webserver-config
name: webserver-config
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [webserver-config, playwright-config, reuseexistingserver, dev-server]
level: practitioner
status: docs-checked
description: "Start the app under test from Playwright's webServer config: command, url readiness, reuseExistingServer, multiple servers, env, and diagnosing startup timeouts."
sources:
  - https://playwright.dev/docs/test-webserver
  - https://playwright.dev/docs/api/class-testconfig#test-config-web-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# webServer config

**Goal:** `npx playwright test` boots the app, waits until it is ready, and shuts it down.

```ts
export default defineConfig({
  webServer: {
    command: 'npm run start',
    url: 'http://127.0.0.1:3000/health',   // polled until the server answers
    reuseExistingServer: !process.env.CI,    // reuse your local dev server
    timeout: 120_000,
    stdout: 'pipe', stderr: 'pipe',
    env: { NODE_ENV: 'test', DATABASE_URL: process.env.TEST_DB! },
  },
  use: { baseURL: 'http://127.0.0.1:3000' },
});
```
Multiple servers (API + front-end):
```ts
webServer: [
  { command: 'npm run api', url: 'http://127.0.0.1:4000/health', name: 'API' },
  { command: 'npm run web', url: 'http://127.0.0.1:3000', name: 'Web' },
],
```
Use `port` instead of `url` when there is no health endpoint; an open port does not prove the app is ready. For a server on a varying port, `wait: { stdout: /Listening on port (?<my_server_port>\d+)/ }` captures it from the output.

## Build vs dev server
Run tests against a production build in CI (`command: 'npm run build && npm run preview'`) to catch build-only bugs; dev servers compile on first request and cause slow first tests.

## Gotchas
- Use the same host in `url` and `baseURL`.
- `stderr` is piped by default in the docs example while `stdout` is ignored; set `stdout: 'pipe'` to see server logs when startup times out.
- Tests share the server's state, so isolate data per test.
- `gracefulShutdown: { signal: 'SIGTERM', timeout: 5000 }` if the server must flush (coverage, DB). Unspecified, the process group is SIGKILLed; Windows ignores this option.

## Verify
CI log shows the server output followed by tests; killing the server mid-run gives connection errors, proving tests used it.

## Checked

2026-10-28. Confirmed in the Playwright Web server page and testConfig.webServer reference: `command`, `url`, `reuseExistingServer`, `timeout`, `stdout`/`stderr`, `env`, `name`, array of servers, `wait.stdout` capture, `gracefulShutdown` signal/timeout semantics (default SIGKILL, ignored on Windows), `baseURL` in `use`.
Removed: the 2xx/3xx/400-403 status range, the IPv6 `::1` claim, and the claim that the server starts once per run rather than per worker (not found in the fetched pages).

Method: documentation only; no commands were run.
