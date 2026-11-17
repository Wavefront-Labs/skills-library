---
id: computing-software.qa-testing-engineering.jest-pytest.jest-matchers-and-asymmetric-matchers
name: jest-matchers-and-asymmetric-matchers
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [jest-matchers, asymmetric-matchers, toequal, tostrictequal, expect-objectcontaining]
level: practitioner
status: verified
description: "Pick the right Jest matcher: toBe vs toEqual vs toStrictEqual, toMatchObject, toThrow, number and string matchers, and asymmetric matchers like expect.objectContaining."
sources:
  - https://jestjs.io/docs/using-matchers
  - https://jestjs.io/docs/expect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matchers

## Equality
| Matcher | Semantics |
|---|---|
| `toBe(x)` | `Object.is`: primitives, same reference |
| `toEqual(x)` | recursive equality; ignores `undefined` properties, array sparseness, class types (ran: `[1,,3]` equals `[1,undefined,3]`, `new A()` equals `{x:1}`) |
| `toStrictEqual(x)` | like toEqual but checks `undefined` props, sparseness, and object types (class instances) |
| `toMatchObject(subset)` | object contains the subset (recursively); arrays inside must match exactly in length (ran: `{r:[1,2]}` vs `{r:[1]}` fails) |

```js
expect(add(0.1, 0.2)).toBeCloseTo(0.3, 5);
expect(user).toMatchObject({ name: 'Ada', roles: expect.arrayContaining(['admin']) });
expect(list).toHaveLength(3);
expect(map).toHaveProperty('a.b[0]', 1);
expect(str).toMatch(/^ord_[a-z0-9]{10}$/);
expect(() => parse('')).toThrow(/empty input/);
await expect(fetchUser(99)).rejects.toThrow(NotFoundError);
```

## Asymmetric matchers
Use inside equality matchers and mock call assertions:
```js
expect(res).toEqual({
  id: expect.any(String),
  createdAt: expect.stringMatching(/^\d{4}-\d{2}-\d{2}T/),
  items: expect.arrayContaining([expect.objectContaining({ sku: 'A1' })]),
  meta: expect.anything(),          // anything except null/undefined (`null` fails, `0` passes)
});
expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('saved'), expect.any(Object));
expect(obj).toEqual(expect.not.objectContaining({ password: expect.anything() }));
```

## Custom matchers
```js
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return { pass, message: () => `expected ${received} ${pass ? 'not ' : ''}to be within ${floor}-${ceiling}` };
  },
});
```
Type them in a `.d.ts` for TypeScript.

## Gotchas
- `toEqual` passes for `{a: undefined}` vs `{}`; use `toStrictEqual` for API response shapes where that matters.
- `toThrow` needs a function wrapper; `expect(parse(''))` throws before expect runs.
- Floating point: never `toBe(0.3)`.
- `expect.assertions(n)` in async tests ensures callbacks actually ran.

## Verify
Mutate one field in the system under test: the matcher's diff output points at exactly that field.
