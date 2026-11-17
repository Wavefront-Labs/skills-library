---
id: computing-software.web-development.bun.test-modifiers-expect
name: test-modifiers-expect
category: computing-software
field: web-development
product: bun
tags: [test-modifiers, test-each, expect-poll, test-failing]
level: practitioner
status: docs-checked
description: "Write bun:test tests with skip, todo, only, failing, runIf and each modifiers, retry and repeats, async timeouts, and expect helpers like poll, soft and assertions."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/writing-tests.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { test, describe, expect } from "bun:test";
test.skipIf(isWindows)("skip on Windows", () => {});
test.failing("known bug", () => { expect(0.1 + 0.2).toBe(0.3); }); // passes while failing
test.each([[1, 2, 3], [4, 5, 9]])("add(%i, %i) = %i", (a, b, c) => expect(a + b).toBe(c));
test("queue drains", async () => { await expect.poll(() => queue.length).toBe(0); });
test("flaky", { retry: 3 }, async () => {});
test("slow", async () => {}, 10_000);   // per-test timeout; default 5000 ms
```

Modifiers: `skip`, `todo` (runs with `bun test --todo`; a passing todo is reported as a failure), `only` (use `bun test --only`), `if`/`runIf`, `skipIf`, `todoIf`, `failing`, `concurrent`. Order of chaining does not matter; `skip` beats `todo`, `todo` beats `failing`.

Helpers: `expect.hasAssertions()`, `expect.assertions(n)`, `expect.soft(v)` (records failure, keeps going), `expect.poll(fn, { interval, timeout })` (defaults 50 ms and 1000 ms; no `.resolves`, `.rejects`, `toThrow()` or snapshots), `.resolves`/`.rejects`.

Gotchas:
- A test taking `done` must call it or it hangs.
- On timeout Bun kills child processes the test spawned.
- `retry` and `repeats` cannot be combined; `repeats: N` runs N+1 times.
- `expect.stringMatching()` treats a string as regex source; use `stringContaining()` for literal text.
- `await` promise matchers if later code depends on them.

## Checked

2026-11-04. Confirmed against the Bun docs page test/writing-tests (and the retry options form on test/index): the modifier list and precedence, test.todo with --todo, test.only with --only, skipIf/todoIf/if/runIf, test.failing inversion, test.each specifiers, timeout default 5000 and zombie process killing, retry and repeats (N+1 runs, not combinable), done callback, expect.soft, expect.poll defaults 50 and 1000 and its unsupported matchers, assertion counting, stringMatching regex-source note. Nothing removed.
Method: documentation only; no commands were run.
