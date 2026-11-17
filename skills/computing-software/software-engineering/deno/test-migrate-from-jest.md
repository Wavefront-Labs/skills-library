---
id: computing-software.software-engineering.deno.test-migrate-from-jest
name: test-migrate-from-jest
category: computing-software
field: software-engineering
product: deno
tags: [test, migration, jest, node-test, std-expect, module-mocks]
level: practitioner
status: docs-checked
description: "Move a Jest suite to deno test: node:test for describe/it, @std/expect matchers, mapping of jest APIs and CLI flags, config, and jest.mock replacements."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/migrate_from_jest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most Jest suites need only new imports. Nothing is a global; `describe`, `it`, `expect` and hooks are explicit imports:

```ts title="cart.test.ts"
import { beforeEach, describe, it } from "node:test";
import { expect, fn } from "jsr:@std/expect";
```

Tests written against `node:test` also still run on Node.js.

| Jest | Deno |
| --- | --- |
| `describe`, `it`, `beforeEach` | `node:test` or `@std/testing/bdd` |
| `expect(...)` | `jsr:@std/expect` |
| `jest.fn()` | `fn()` from `jsr:@std/expect` |
| `jest.spyOn(obj, "m")` | `spy`/`stub` from `@std/testing/mock` |
| `toMatchSnapshot()` | `assertSnapshot` |
| `jest.useFakeTimers()` | `FakeTime` |
| `npx jest` | `deno test` |
| `npx jest --watch` | `deno test --watch` |
| `npx jest -t "name"` | `deno test --filter "name"` |

Config mostly disappears: TypeScript, JSX and ES modules need no transforms, so `ts-jest`, `babel-jest` and `transform` have no equivalent. File selection goes in deno.json:

```json title="deno.json"
{
  "test": {
    "include": ["src/**/*.test.ts"],
    "exclude": ["src/fixtures/"]
  }
}
```

There is no `jest.mock("./module")` equivalent here because module records are immutable in Deno. Migrate to dependency injection (pass a spy or stub in) or stub the object the module exposes. This is usually the only part needing changes to code under test.

npm test helpers still work via `npm:` specifiers.

## Checked

2026-11-04. Confirmed against docs runtime/test/migrate_from_jest.md: imports, Jest-to-Deno mapping table, config translation, jest.mock replacement.

Method: documentation only; no commands were run.
