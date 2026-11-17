---
id: computing-software.software-engineering.deno.test-steps-timeouts-retries
name: test-steps-timeouts-retries
category: computing-software
field: software-engineering
product: deno
tags: [test, test-steps, timeout, retry, repeats, flaky-tests]
level: practitioner
status: docs-checked
description: "Break a Deno test into t.step steps, set per-test timeouts, and use retry and repeats (and the --retry/--repeats flags) to tolerate or detect flakiness."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps break a test into parts:

```ts
Deno.test("database operations", async (t) => {
  using db = await openDatabase();
  await t.step("insert user", async () => {
    // Insert user logic
  });
  await t.step("insert book", async () => {
    // Insert book logic
  });
});
```

`timeout` (ms) fails a test that exceeds it, catching hung promises and synchronous hot loops. The next test still runs. `0` or omitted means no deadline.

```ts
Deno.test({
  name: "completes within deadline",
  timeout: 5000,
  async fn() {
    const response = await fetch("https://example.com");
    await response.body?.cancel();
  },
});
```

`retry` re-runs a failing test and passes if any attempt passes; `repeats` runs it several times and requires every run to pass:

```ts
Deno.test({
  name: "flaky network call",
  retry: 3, // re-run up to 3 times; pass if any attempt passes
  async fn() {},
});

Deno.test({
  name: "must be deterministic",
  repeats: 5, // run 5 times; fail if any run fails
  fn() {},
});
```

They compose. Every attempt re-runs `beforeEach`/`afterEach` hooks and takes a fresh leak-check baseline, so resource leaks are retried too.

`deno test --retry=2` (and `--repeats`) set run-wide defaults; a test's own option wins, including an explicit `0`.

## Checked

2026-11-04. Confirmed against docs runtime/test/index.md (Testing): t.step, timeout (0 or omitted means no deadline), retry, repeats, hook and leak-baseline behaviour, --retry flag and per-test precedence.

Method: documentation only; no commands were run.
