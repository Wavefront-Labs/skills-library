---
id: computing-software.software-engineering.deno.test-writing-and-running
name: test-writing-and-running
category: computing-software
field: software-engineering
product: deno
tags: [test, deno-test, assertions, test-discovery, parallel, node-test]
level: intro
status: docs-checked
description: "Write tests with Deno.test and std assertions, run deno test with discovery globs, parallel and args, and choose between Deno.test and node:test."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts title="my_test.ts"
import { assertEquals } from "jsr:@std/assert";
import { delay } from "jsr:@std/async";

Deno.test("simple test", () => {
  assertEquals(1 + 2, 3);
});

Deno.test("async test", async () => {
  await delay(100);
  assertEquals(1 + 2, 3);
});

Deno.test({
  name: "read file test",
  fn: () => {
    const data = Deno.readTextFileSync("./somefile.txt");
    assertEquals(data, "expected content");
  },
});
```

Prefer Jest-style? Use `import { expect } from "jsr:@std/expect"` and `expect(result).toBe(5)`.

`deno test` with no argument finds files matching `{*_,*.,}test.{ts, tsx, mts, js, mjs, jsx}` recursively; any script inside a `__tests__` directory is also a test file.

```sh
deno test                      # everything
deno test util/                # one directory
deno test my_test.ts           # one file
deno test --parallel           # run test modules in parallel
deno test my_test.ts -- -e --foo --bar   # visible in Deno.args
deno test --allow-read=. my_test.ts
```

`Deno.test` and `node:test` are both first-class: `deno test` discovers either, and you can mix them. Use `node:test` for suites portable to Node (its `mock.timers` and `mock.module` work); use `Deno.test` for per-test permissions and sanitizer toggles.

## Checked

2026-11-04. Confirmed against docs runtime/test/index.md (Testing): Deno.test examples, @std/expect, test discovery glob and __tests__ rule, deno test invocations, Deno.test vs node:test and mock.timers/mock.module.

Method: documentation only; no commands were run.
