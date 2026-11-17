---
id: computing-software.software-engineering.deno.test-per-test-permissions
name: test-per-test-permissions
category: computing-software
field: software-engineering
product: deno
tags: [test, permissions, deny-permissions, fallbacks, bdd, describe-it]
level: advanced
status: docs-checked
description: "Use the Deno.test permissions option to deny or narrow permissions per test (it never grants), plus BDD describe/it from @std/testing."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `permissions` property on `Deno.test` can deny permissions but never grants them; they must be passed on the command line. Use it to test fallbacks when access is missing. No `permissions` means inherit.

```ts
Deno.test({
  name: "File reader falls back to error message without permission",
  permissions: { read: false },
  fn: async () => {
    const result = await getFileText();
    assertEquals(result, "oops don't have permission");
  },
});
```

Run with the flags the permitted tests need: `deno test --allow-read`.

Detailed form:

```ts
Deno.test({
  name: "permission configuration example",
  permissions: {
    read: ["./data", "./config"], // Grant read to specific paths only
    write: false, // Explicitly deny write permissions
    net: ["example.com:443"], // Allow specific host:port combinations
    env: ["API_KEY"], // Allow access to specific env variables
    run: false, // Deny subprocess execution
    ffi: false, // Deny loading dynamic libraries
  },
  fn() {},
});
```

Anything not granted at the command line is denied regardless of the test config.

BDD style with `@std/testing/bdd`:

```ts
import { describe, it } from "jsr:@std/testing/bdd";
import { expect } from "jsr:@std/expect";

describe("add function", () => {
  it("adds two numbers correctly", () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

## Checked

2026-11-04. Confirmed against docs runtime/test/index.md (Testing): permissions option denies but never grants, detailed permissions object, @std/testing/bdd describe/it.

Method: documentation only; no commands were run.
