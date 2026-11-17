---
id: computing-software.qa-testing-engineering.vitest.type-testing-expect-typeof
name: type-testing-expect-typeof
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [type-testing, expect-type-of, assert-type, typecheck]
level: practitioner
status: docs-checked
description: "Test TypeScript types in Vitest with expectTypeOf and assertType in *.test-d.ts files, run them with --typecheck, and read the Expected/Actual error messages."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/testing-types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Files matching `*.test-d.ts` are type tests (change with `typecheck.include`). Vitest does not run them; the compiler analyses them statically, so dynamic names or `test.each` titles are shown as written.

```ts
// mount.test-d.ts
import { assertType, expectTypeOf } from 'vitest'
import { mount } from './mount.js'

test('my types work properly', () => {
  expectTypeOf(mount).toBeFunction()
  expectTypeOf(mount).parameter(0).toExtend<{ name: string }>()

  // @ts-expect-error name is a string
  assertType(mount({ name: 42 }))
})
```

Enable with the flag, e.g. `"test": "vitest --typecheck"`. Vitest runs `tsc --noEmit` (or `vue-tsc --noEmit`), so you can drop those from your pipeline. Source-code type errors are reported too; turn that off with `typecheck.ignoreSourceErrors`. `--allowOnly` and `-t` work with typechecking.

Reading errors: for a failed `toEqualTypeOf`, look at the property name and the message `Expected: string, Actual: number`. Prefer a type argument (`toEqualTypeOf<{ a: string }>()`) over a concrete value, and compare two values with `toEqualTypeOf<typeof two>()`.

A `@ts-expect-error` can hide a typo (a misspelled variable is still an error, so the check passes). Include the type files in `test.include` so Vitest also runs them and fails with `ReferenceError`.

## Checked

2026-11-04. Confirmed against guide/testing-types.md: `*.test-d.ts` and `typecheck.include`, static analysis only, the sample test, `--typecheck`, `tsc --noEmit` or `vue-tsc --noEmit`, `typecheck.ignoreSourceErrors`, `--allowOnly` and `-t`, the Expected/Actual error reading advice, typeargs versus concrete values, and the `@ts-expect-error` tip.

Method: documentation only; no commands were run.
