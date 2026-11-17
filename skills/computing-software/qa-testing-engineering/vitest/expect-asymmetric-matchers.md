---
id: computing-software.qa-testing-engineering.vitest.expect-asymmetric-matchers
name: expect-asymmetric-matchers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [asymmetric-matchers, object-containing, expect-any, schema-matching]
level: practitioner
status: docs-checked
description: "Match parts of a value with Vitest asymmetric matchers: anything, any, arrayContaining, objectContaining, stringContaining, stringMatching, closeTo, schemaMatching."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Asymmetric matchers go inside `toEqual`, `toHaveBeenCalledWith` and similar to ignore the volatile parts.

```ts
expect(user).toEqual({
  id: expect.any(Number),
  name: expect.stringContaining('Ann'),
  tags: expect.arrayContaining(['admin']),
  meta: expect.objectContaining({ active: true }),
  score: expect.closeTo(0.3, 5),
})
```

- `expect.anything()`: any value except null or undefined.
- `expect.any(Constructor)`: true when the value is an instance of the constructor.
- `expect.arrayContaining`, `expect.objectContaining`.
- `expect.stringContaining`, `expect.stringMatching` (a substring or a regular expression).
- `expect.closeTo(expected, precision?)`: for floats inside objects or arrays; precision is the number of digits after the decimal point, default 2. For a bare number use `toBeCloseTo`.
- `expect.schemaMatching(schema)`: the schema must implement Standard Schema v1 (the docs show Zod, Valibot and ArkType).
- `expect.not.arrayContaining(...)` and the other containing matchers negate.

Custom matchers added with `expect.extend` also become asymmetric matchers.

## Checked

2026-11-04. Confirmed against api/expect.md: each matcher's description, closeTo precision and default, schemaMatching and Standard Schema v1, `expect.not`, `expect.extend`. Removed the second source URL (a recipes page that does not exist) and a closing line about matching one level of intent that the page does not state.

Method: documentation only; no commands were run.
