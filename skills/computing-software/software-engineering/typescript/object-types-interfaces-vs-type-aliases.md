---
id: computing-software.software-engineering.typescript.object-types-interfaces-vs-type-aliases
name: object-types-interfaces-vs-type-aliases
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, interfaces-vs-types, index-signatures, readonly, optional-properties, excess-property-checks, typescript-types]
level: practitioner
status: docs-checked
description: "Model object shapes in TypeScript: interface vs type alias, optional and readonly props, index signatures and Record, excess property checks, and extending/intersecting types."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/objects.html
  - https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces
  - https://www.typescriptlang.org/tsconfig/#noUncheckedIndexedAccess
  - https://www.typescriptlang.org/tsconfig/#exactOptionalPropertyTypes
  - https://github.com/microsoft/TypeScript/wiki/Performance
  - https://typescript-eslint.io/rules/consistent-type-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object types: interfaces vs type aliases

**Goal:** object types that catch typos and missing fields, with the right tool for
extension and dictionaries.

## interface vs type
```ts
interface User { id: string; name: string; email?: string }
interface Admin extends User { permissions: string[] }

type Point = { x: number; y: number };
type Shape = Circle | Square;                 // unions: only `type` can do this
type WithTimestamps<T> = T & { createdAt: Date; updatedAt: Date };
```
| | interface | type |
|---|---|---|
| unions, tuples, mapped/conditional types | no | yes |
| declaration merging (augmenting libs) | yes | no |
| `extends` error messages / perf on deep hierarchies | better | intersections can be slower |
Rule of thumb: `interface` for object shapes others may extend or augment; `type` for
everything else. Consistency within a codebase matters more than the choice
(`@typescript-eslint/consistent-type-definitions`).

## Optional, undefined and readonly
```ts
interface Config {
  readonly apiUrl: string;          // shallow: nested objects still mutable
  retries?: number;                 // may be absent
  timeout: number | undefined;      // must be present, may be undefined
}
const tags: readonly string[] = ["a"];   // or ReadonlyArray<string>; no push/splice
```
With `exactOptionalPropertyTypes`, `retries?: number` no longer accepts an explicit
`undefined` - distinguishes "absent" from "set to undefined" (matters for PATCH payloads).
`as const` for deep literal immutability of literals at compile time; `Readonly<T>` is shallow.

## Index signatures and Record
```ts
interface Headers { [name: string]: string }
type Scores = Record<string, number>;
type ByRole = Record<"admin" | "user", User[]>;     // exhaustive keys required
const m = new Map<string, User>();                  // prefer Map for dynamic keys + frequent adds/deletes
```
Turn on `noUncheckedIndexedAccess`: `scores["bob"]` becomes `number | undefined`, forcing a check
- catches the most common runtime crash with dictionaries.

## Excess property checks
```ts
const u: User = { id: "1", name: "A", emial: "x" };   // error: object literal may only specify known properties
const raw = { id: "1", name: "A", emial: "x" };
const u2: User = raw;                                 // no error! check applies to fresh literals only
```
Structural typing means extra properties pass when not a literal - validate external data at
runtime instead of trusting assignment.

## Extending vs intersecting
The handbook notes that interfaces and intersections differ in how conflicts are handled; the TypeScript performance guide suggests `interface ... extends` over intersections for hierarchies.

## Verify
- [ ] `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` evaluated for the project.
- [ ] Public types use `readonly` where callers must not mutate.

## Checked
Checked 2026-10-25 against the TypeScript-Website handbook, tsconfig reference, TypeScript performance wiki and bundled lib.es5.d.ts. Confirmed: a type alias cannot be re-opened while an interface can; `readonly` is shallow; excess property checks apply to fresh object literals; ReadonlyArray; noUncheckedIndexedAccess adds undefined; exactOptionalPropertyTypes (4.4, not part of strict); Record with literal key unions; the consistent-type-definitions rule; extending interfaces is recommended over intersections for performance. Removed the unconfirmed claim that an intersection silently yields never and the named validator.
Method: documentation only; no commands were run.
