---
id: computing-software.qa-testing-engineering.vitest.test-each-for
name: test-each-for
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-each, test-for, parameterized-tests, printf-format]
level: practitioner
status: docs-checked
description: "Write parameterized Vitest tests with test.each and test.for, printf-style titles, $prop interpolation and tagged-template tables, and know how they differ."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/test.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
test.each([
  [1, 1, 2],
  [1, 2, 3],
])('add(%i, %i) -> %i', (a, b, expected) => {
  expect(a + b).toBe(expected)
})

test.each([{ a: 1, b: 1, sum: 2 }])('add($a, $b) -> $sum', ({ a, b, sum }) => {
  expect(a + b).toBe(sum)
})

test.each`
  a    | b    | expected
  ${1} | ${1} | ${2}
`('returns $expected when $a + $b', ({ a, b, expected }) => {
  expect(a + b).toBe(expected)
})
```

Title formats: `%s` string, `%d` number, `%i` integer, `%f` float, `%j` JSON, `%o` object, `%#` case index, `%$` case number, `%%` literal percent.

`test.for` is the same idea but does not spread array cases: each case arrives as one argument, and the test context is passed as the second argument.

```ts
test.for([[1, 1, 2]])('add %i', ([a, b, expected], { expect }) => {
  expect(a + b).toBe(expected)
})
```

`test.each` spreads array cases into arguments; `test.for` does not, and passes the test context as the second argument (for example for concurrent snapshots). Non-array arguments, including the template-string form, work the same in both.

## Checked

2026-11-04. Confirmed against api/test.md: the printf specifiers and their meanings, `$prop`, `$0` and `$a.val` interpolation, the tagged-template table, and the `test.each` versus `test.for` difference with the context argument.

Method: documentation only; no commands were run.
