---
id: computing-software.qa-testing-engineering.jest-pytest.jest-each-table-tests
name: jest-each-table-tests
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [jest-each, test-each, describe-each, parameterized-tests-jest, data-driven-testing-jest]
level: practitioner
status: verified
description: "Write table-driven tests with Jest test.each and describe.each: array and tagged-template tables, printf-style titles, object interpolation and concurrent each."
sources:
  - https://jestjs.io/docs/api#testeachtablename-fn-timeout
  - https://jestjs.io/docs/api#describeeachtablename-fn-timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# test.each tables

## Array table
```js
test.each([
  [1, 1, 2],
  [1, 2, 3],
  [2, 1, 3],
])('add(%i, %i) -> %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```
Format specifiers: `%s` string, `%d`/`%i` number, `%f`, `%j` JSON, `%o` object, `%p` pretty-format, `%#` 0-based index, `%$` 1-based number (ran on Jest 30: titles `add(1, 1) -> 2 #0 $1`). Placeholders beyond the row's arguments stay literal.

## Objects with named interpolation
```js
test.each([
  { input: '', error: 'required' },
  { input: 'a@', error: 'invalid' },
])('email "$input" -> $error', ({ input, error }) => {
  expect(validateEmail(input)).toBe(error);
});
```
Nested paths work: `$user.name`.

## Tagged template table
```js
test.each`
  amount | currency | expected
  ${0}   | ${'NZD'} | ${'$0.00'}
  ${1e6} | ${'JPY'} | ${'¥1,000,000'}
`('formats $amount $currency', ({ amount, currency, expected }) => {
  expect(formatMoney(amount, currency)).toBe(expected);
});
```

## describe.each
```js
describe.each(['sqlite', 'postgres'])('repo on %s', (driver) => {
  let repo;
  beforeAll(async () => { repo = await makeRepo(driver); });
  test('saves', async () => { ... });
});
```

## Variants
`test.only.each`, `test.skip.each`, `test.concurrent.each` (async tests in parallel within the file; mind shared state).

## Gotchas
- A 1D array of arrays is spread as arguments; a 1D array of primitives passes one argument each: `test.each([1, 2])('%i', (n) => ...)`.
- Duplicate titles make failures ambiguous; include enough fields or `%#`.
- Large tables hide intent: group by partition/boundary with comments.

## Verify
`npx jest -t "email"` shows each row as a separate named test.
