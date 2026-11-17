---
id: computing-software.software-engineering.typescript.testing-types-with-expect-type-and-tsd
name: testing-types-with-expect-type-and-tsd
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-testing, type-testing, expect-type, tsd, ts-expect-error, dtslint, library-types]
level: practitioner
status: docs-checked
description: "Test TypeScript types as rigorously as runtime code: expect-type/Vitest typecheck, tsd, @ts-expect-error assertions, and type tests for public library APIs in CI."
sources:
  - https://github.com/mmkal/expect-type#readme
  - https://vitest.dev/guide/testing-types.html
  - https://github.com/tsdjs/tsd#readme
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html#-ts-expect-error-comments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing types with expect-type and tsd

**Goal:** public types (generics, overloads, inference from arguments) are locked down by tests, so refactors cannot silently loosen them to `any`.

## 1. @ts-expect-error: the zero-dependency baseline
```ts
// types.test-d.ts (only type-checked, never executed)
import { route } from "../src";
route("/users/:id", p => p.id satisfies string);
// @ts-expect-error - unknown param
route("/users/:id", p => p.nope);
```
`@ts-expect-error` fails compilation if the next line does **not** error, unlike `@ts-ignore`. Run with `tsc --noEmit -p tsconfig.test.json`.

## 2. expect-type (works with any runner; built into Vitest)
```ts
import { expectTypeOf } from "expect-type";        // or from "vitest"
expectTypeOf(parse("1")).toEqualTypeOf<number>();
expectTypeOf(useQuery).parameter(0).toExtend<{ key: string[] }>();
expectTypeOf<Getters<{ a: 1 }>>().toEqualTypeOf<{ getA: () => 1 }>();
expectTypeOf(api.get).returns.resolves.toEqualTypeOf<User>();
expectTypeOf(parse("1")).not.toBeAny();             // detects any leaks
```
`toEqualTypeOf` is exact (catches `any` and extra properties); `toExtend` (replacing the deprecated `toMatchTypeOf`) checks that a type extends the expected one.

Vitest: files named `*.test-d.ts` run with `vitest --typecheck`, reporting type errors as test failures.

## 3. tsd (for published packages)
```ts
// index.test-d.ts
import { expectType, expectError, expectAssignable } from "tsd";
import pick from ".";
expectType<{ a: number }>(pick({ a: 1, b: 2 }, ["a"]));
expectError(pick({ a: 1 }, ["z"]));
```
`npx tsd` finds the `.d.ts` named by the `types` field of `package.json` and type-checks `*.test-d.ts` files against it.

## 4. What to test
- Inference: return types follow arguments (generic propagation, overload selection).
- Rejections: invalid calls fail (`@ts-expect-error`/`expectError`).
- No `any` leakage on public API boundaries.
- Compatibility across supported TypeScript versions: run the type tests against each supported TypeScript version in a CI matrix.

## Gotchas
- Type test files must be included by the tsconfig used in CI, but excluded from the build output.
- `toEqualTypeOf` error messages can be long; see the "Error messages" section of the expect-type README.
- Intersection types are a known limitation of `toEqualTypeOf`; for simple cases normalise with a mapped type (`type Simplify<T> = {[K in keyof T]: T[K]}`).
- Overly strict type tests on internal helpers slow refactoring; focus on the public surface.

## Verify
- Loosen a public signature to `any` deliberately: the type tests fail in CI.

## Checked
Checked 2026-10-25 against the expect-type README, the Vitest testing-types guide, the tsd README and the TypeScript 3.9 release notes. Confirmed: `@ts-expect-error` fails when the next line does not error (3.9); expect-type `toEqualTypeOf`, `.parameter(0)`, `.returns`, `.resolves`, `.not.toBeAny()`; `toMatchTypeOf` is deprecated in favour of `toExtend`; the intersection limitation and mapped-type workaround; Vitest runs `*.test-d.ts` files with the `--typecheck` flag and exposes `expectTypeOf`; tsd's `expectType`, `expectError`, `expectAssignable` and its use of the `types` field of package.json. Removed the unconfirmed `typecheck.enabled` setting, `typesVersions` advice and the `toEqualTypeOf<unknown>` any-detector.
Method: documentation only; no commands were run.
