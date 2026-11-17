---
id: computing-software.qa-testing-engineering.jest-pytest.fast-check-property-based-js
name: fast-check-property-based-js
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [fast-check-arbitraries, fast-check, property-based-testing-js, shrinking, fc-assert]
level: practitioner
status: verified
description: "Write property-based tests in JavaScript/TypeScript with fast-check: arbitraries, fc.assert/fc.property, preconditions, shrinking, replaying seeds and model-based commands."
sources:
  - https://fast-check.dev/docs/introduction/
  - https://fast-check.dev/docs/core-blocks/arbitraries/
  - https://fast-check.dev/docs/advanced/model-based-testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based testing in JS with fast-check

```ts
import fc from 'fast-check';

test('decode(encode(x)) === x', () => {
  fc.assert(fc.property(fc.string(), (s) => {
    expect(decode(encode(s))).toBe(s);
  }));
});

test('sort is idempotent and ordered', () => {
  fc.assert(fc.property(fc.array(fc.integer()), (xs) => {
    const once = sortNums(xs);
    expect(sortNums(once)).toEqual(once);
    for (let i = 1; i < once.length; i++) expect(once[i - 1]).toBeLessThanOrEqual(once[i]);
  }), { numRuns: 500 });
});
```
Integration: `@fast-check/jest` or `@fast-check/vitest` give `test.prop([fc.string()])('...', (s) => ...)` (both ran). Default is 100 runs per property.

## Arbitraries
`fc.integer({ min, max })`, `fc.double({ noNaN: true })`, `fc.string({ minLength: 1 })`, `fc.emailAddress()`, `fc.uuid()`, `fc.date()`, `fc.array(arb, { maxLength: 50 })`, `fc.record({ id: fc.uuid(), qty: fc.nat(100) })`, `fc.oneof(...)`, `fc.constantFrom('NZD', 'USD')`, `fc.tuple(...)`.
Transform: `.map(f)`, `.filter(pred)` (keep rejection rare), `.chain(x => arbDependingOn(x))`.
Preconditions: `fc.pre(b !== 0)` inside the property. Too many rejected runs fail with "Failed to run property, too many pre-condition failures encountered" (ran).

## Failures and replay
On failure fast-check shrinks to a minimal counterexample and prints `{ seed, path, endOnFailure: true }` (ran on fast-check 4.10: "Property failed after 2 tests", "Counterexample: [[2,1000000000]]", "Shrunk 75 time(s)"); passing that object back replays the failure in one run:
```ts
fc.assert(prop, { seed: -1819918769, path: '0:1:0', endOnFailure: true });
```
Add the counterexample as a regular example test too (`examples: [[42]]` option runs those inputs first; ran).

## Model-based (stateful)
Define commands (`check(model)`, `run(model, real)`) and run `fc.assert(fc.property(fc.commands([...]), cmds => fc.modelRun(setup, cmds)))` to find sequences breaking invariants (e.g. a cache vs a Map model).

## Good properties
Round-trip, idempotence, invariants (length preserved, totals conserved), oracle comparison with a simple reference implementation, metamorphic relations.

## Gotchas
- Properties that re-implement the function under test prove nothing.
- Async properties: `fc.asyncProperty` and `await fc.assert(...)`.
- A very selective `filter` makes generation slow or endless (`fc.integer().filter(x => x === 123456)` never finished here); `fc.pre` gives the "too many pre-condition failures" error instead. Construct valid values with `map` instead.

## Verify
Introduce an off-by-one in the code: fast-check reports a shrunk counterexample within default runs.
