---
id: computing-software.software-engineering.deno.test-each-and-hooks
name: test-each-and-hooks
category: computing-software
field: software-engineering
product: deno
tags: [test, test-each, parameterized, hooks, before-each, after-all]
level: practitioner
status: docs-checked
description: "Parameterized tests with Deno.test.each name templates and the beforeAll/beforeEach/afterEach/afterAll hooks with their FIFO/LIFO order."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Deno.test.each` registers one real test per case, each filterable on its own. Array cases spread as positional arguments; name tokens are `%s`, `%d`/`%i`, `%f`, `%j`, `%o`/`%O`, and `%#` for the zero-based index.

```ts
Deno.test.each([
  [1, 1, 2],
  [2, 3, 5],
])("add(%i, %i) = %i", (a, b, expected) => {
  assertEquals(a + b, expected);
});
```

Object cases are one argument; `$key` and `$key.nested` interpolate properties:

```ts
Deno.test.each([
  { a: 1, b: 1, sum: 2 },
  { a: 2, b: 3, sum: 5 },
])("$a + $b = $sum", ({ a, b, sum }) => {
  assertEquals(a + b, sum);
});
```

Compose with `.only.each` and `.ignore.each`.

Hooks:

- `Deno.test.beforeAll(fn)` once before all tests in scope
- `Deno.test.beforeEach(fn)` before each test
- `Deno.test.afterEach(fn)` after each test
- `Deno.test.afterAll(fn)` once after all tests

`beforeAll`/`beforeEach` run FIFO; `afterEach`/`afterAll` run LIFO. If a hook throws, remaining hooks of that type do not run and the current test fails. Several hooks of one type may be registered.

```ts
Deno.test.beforeEach(() => {
  console.log("First beforeEach hook");
});

Deno.test.beforeEach(() => {
  console.log("Second beforeEach hook");
});
```

## Checked

2026-11-04. Confirmed against docs runtime/test/index.md (Testing): Deno.test.each tokens and templates, .only.each/.ignore.each, the four hooks, FIFO/LIFO order, hook-failure behaviour.

Method: documentation only; no commands were run.
