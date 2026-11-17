---
id: computing-software.qa-testing-engineering.vitest.expect-equality-matchers
name: expect-equality-matchers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [expect, to-be, to-equal, to-strict-equal]
level: intro
status: docs-checked
description: "Pick the right Vitest equality matcher: toBe uses Object.is, toEqual and toStrictEqual compare deeply, plus toMatchObject, toHaveProperty and toContainEqual."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitest `expect` is Chai-based with Jest-compatible matchers. A message can be passed as the second argument: `expect(value, 'why it matters')`.

- `toBe(x)`: primitives and reference identity, using `Object.is`.
- `toEqual(x)`: deep equality.
- `toStrictEqual(x)`: deep equality that is also strict about types and structure.
- `toMatchObject(subset)`: object contains the given properties.
- `toContain(item)`: the item is in an array (or a string contains a substring); `toContainEqual(item)`: an item with that structure and values is in an array.
- `toHaveLength(n)`.
- `toHaveProperty(path, value?)`: pass an array path to avoid dot parsing.
- `toMatch(stringOrRegExp)` for strings.
- `toSatisfy(fn)` for a custom predicate.

```ts
expect({ a: 1, b: { c: 2 } }).toMatchObject({ b: { c: 2 } })
expect({ 'a.b': 1 }).toHaveProperty(['a.b'], 1)
```

Related checks: `toBeNull`, `toBeUndefined`, `toBeDefined`, `toBeTruthy`, `toBeFalsy`, `toBeNaN`, `toBeTypeOf`, `toBeInstanceOf`, `toBeOneOf`, `toBeCloseTo` (floats), and numeric comparisons.

`toThrow` needs the code wrapped in a function: `expect(() => fn()).toThrow()`.

## Checked

2026-11-04. Confirmed against api/expect.md: chai plus Jest-compatible matchers and the message argument, `toBe` with `Object.is`, `toEqual`, `toStrictEqual`, `toContain`, `toContainEqual`, `toHaveProperty` array path, `toBeOneOf`, `toBeTypeOf`, `toSatisfy`, and the wrap-in-a-function rule for `toThrow`.

Method: documentation only; no commands were run.
