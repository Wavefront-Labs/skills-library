---
id: computing-software.software-engineering.typescript.typescript-classes-and-modifiers
name: typescript-classes-and-modifiers
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-classes, access-modifiers, private-fields, abstract-classes, parameter-properties, implements]
level: practitioner
status: docs-checked
description: "Write TypeScript classes correctly: private vs #private, parameter properties, readonly, abstract classes, implements vs extends, override, and strictPropertyInitialization."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/classes.html
  - https://www.typescriptlang.org/tsconfig/#strictPropertyInitialization
  - https://www.typescriptlang.org/tsconfig/#noImplicitOverride
  - https://www.typescriptlang.org/tsconfig/#erasableSyntaxOnly
  - https://www.typescriptlang.org/tsconfig/#useDefineForClassFields
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#auto-accessors-in-classes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypeScript classes and modifiers

**Goal:** classes whose encapsulation actually holds and whose types match runtime
behaviour.

## Fields and initialisation
```ts
class Cache<V> {
  #store = new Map<string, V>();               // ECMAScript private: enforced at runtime
  private hits = 0;                             // TS private: compile-time only, visible in JS
  readonly createdAt = Date.now();
  declare readonly kind: "cache";              // type-only, no emitted field
  ttl!: number;                                 // definite assignment: "I set it elsewhere"
  constructor(private readonly name: string, public max = 100) {}   // parameter properties
}
```
- `strictPropertyInitialization` (strict) requires every field to be assigned in the
  constructor; `!` opts out per field - use sparingly (DI frameworks, `init()` patterns).
- `#private` fields are hard private (not reachable through bracket-notation escape hatches); `private` is a compile-time check only. Use `#` for true
  encapsulation in libraries; `private` is fine within an app.
- Parameter properties are not erasable syntax: with Node type stripping or
  `erasableSyntaxOnly`, write explicit fields.

## Modifiers
`public` (default), `protected` (subclasses), `private`, `static`, `readonly`, `abstract`,
`override`, `accessor` (auto-accessors with decorators).

## implements vs extends
```ts
interface Clock { now(): Date }
class SystemClock implements Clock { now() { return new Date(); } }   // checks shape only, inherits nothing
abstract class Repo<T> {
  abstract find(id: string): Promise<T | undefined>;
  async get(id: string): Promise<T> {
    const x = await this.find(id);
    if (!x) throw new NotFoundError(id);
    return x;
  }
}
```
`implements` does not contextually type method parameters - annotate them.

## override
With `noImplicitOverride`, overriding requires the `override` keyword; renaming a base method
then breaks subclasses at compile time instead of silently creating a new method.

## Gotchas
- Methods lose `this` when passed as callbacks (`arr.map(obj.method)`): use arrow-function
  fields (`handle = () => {...}`, one copy per instance) or `.bind`.
- Classes are structurally typed: an object literal with the same public shape is assignable.
- `useDefineForClassFields` (on when `target` is ES2022 or later) initialises fields after the parent
  constructor completes, which changes behaviour for fields redeclared in subclasses.
- Prefer plain functions and object types for data; classes for stateful behaviour.

## Verify
- [ ] `strict` + `noImplicitOverride` enabled.
- [ ] Library classes use `#private` for state that must not leak.

## Checked
Checked 2026-10-25 against the TypeScript-Website Classes handbook, tsconfig reference and 4.9 release notes. Confirmed: `declare` type-only field declarations; `!` definite assignment; `#private` as hard private; parameter properties; `implements` does not change the class or its method types; abstract classes; `override` with noImplicitOverride; erasableSyntaxOnly rejecting parameter properties, enums and runtime namespaces; fields initialised after the parent constructor when `target` is ES2022 or later or useDefineForClassFields is true; auto-accessors (4.9). Removed unconfirmed claims about JSON tooling, nominal behaviour with private members and Object.defineProperty shadowing.
Method: documentation only; no commands were run.
