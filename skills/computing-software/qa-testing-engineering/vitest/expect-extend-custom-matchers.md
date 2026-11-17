---
id: computing-software.qa-testing-engineering.vitest.expect-extend-custom-matchers
name: expect-extend-custom-matchers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [expect-extend, custom-matchers, equality-testers, matchers-types]
level: advanced
status: docs-checked
description: "Add custom Vitest matchers with expect.extend, load them from setupFiles, type them by augmenting Matchers, and add equality testers with expect.addEqualityTesters."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/extending-matchers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
// vitest.setup.ts (listed in setupFiles)
import { expect } from 'vitest'

expect.extend({
  toBeWithin(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling
    return {
      pass,
      message: () => `expected ${received} ${pass ? 'not ' : ''}to be within ${floor}-${ceiling}`,
    }
  },
})
```

```ts
// vitest.d.ts (ambient declaration file)
import 'vitest'

declare module 'vitest' {
  interface Matchers<R, T> {
    toBeWithin: (floor: number, ceiling: number) => R
  }
}
```

`R` is the assertion return type and `T` the type of the received value. The `import 'vitest'` makes the file a module, without which the declaration does not work.

- Call `expect.extend` inside `setupFiles` if you want the matchers in every test.
- A matcher returns `{ pass, message }` where `message` is a function; optional `actual` and `expected` appear in the diff. Do not alter `pass` for `.not`: Vitest reverses it (`this.isNot` is available).
- An async matcher should be declared as returning `Promise<void>` and awaited in the test.
- Custom matchers also work as asymmetric matchers.
- `expect.addEqualityTesters([fn])` teaches `toEqual` and friends how to compare custom types.
- `expect.addSnapshotSerializer` adds custom snapshot serializers; call it inside `setupFiles`.

Include the ambient declaration file in your `tsconfig.json`.

## Checked

2026-11-04. Confirmed against api/expect.md (`expect.extend`, setupFiles tip, `Matchers<R, T>` augmentation, `expect.addEqualityTesters`, `expect.addSnapshotSerializer`) and guide/extending-matchers.md (result shape, `isNot`, async matchers, tsconfig warning). Corrected the type augmentation, which used a `Matchers<T = any>` form the pages do not show, and removed a claim that a missing tsconfig include still lets the matcher run.

Method: documentation only; no commands were run.
