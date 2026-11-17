---
id: computing-software.software-engineering.typescript.generics-and-type-narrowing
name: generics-and-type-narrowing
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, generics, type-narrowing, discriminated-unions, type-guards, conditional-types, infer, satisfies, control-flow-analysis, unknown, type-predicates, typescript-generics]
level: advanced
status: docs-checked
description: "Write TypeScript generics and narrow unions with type guards and discriminated unions so the compiler catches bugs instead of forcing any/as casts."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/generics.html
  - https://www.typescriptlang.org/docs/handbook/2/narrowing.html
  - https://www.typescriptlang.org/docs/handbook/2/conditional-types.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html#preserved-narrowing-in-closures-following-last-assignments
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Generics and type narrowing — let the compiler do the checking

**Goal:** write functions and unions where TypeScript's control-flow analysis proves
correctness, instead of reaching for `as` or `any` whenever the type gets hard.

## 1. Discriminated unions, not optional-field soup
```ts
// Bad: every consumer has to check 3 fields to know which case it is
type Result = { ok: boolean; data?: Data; error?: string };

// Good: one tag, compiler narrows automatically
type Result =
  | { kind: "ok"; data: Data }
  | { kind: "error"; error: string };

function handle(r: Result) {
  if (r.kind === "ok") r.data;      // narrowed, .error not accessible here
  else r.error;                     // narrowed to the error branch
}
```
This is the single highest-leverage TS pattern: it turns a runtime "which fields are
set" question into a compile-time exhaustiveness check. Add a `default: never`
switch-case guard so adding a new union member fails the build until every switch
handles it:
```ts
default: { const _exhaustive: never = r; throw new Error("unhandled"); }
```

## 2. Generic constraints, not `any`
```ts
function pluck<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }
```
`K extends keyof T` ties the return type to the actual key — callers get the real
field type back, and typo'd keys fail at the call site instead of returning `undefined`
silently. Default generic params (`<T = Default>`) remove the need to annotate at
every call site when the common case dominates.

## 3. `infer` for pulling types out of other types
```ts
type ElementOf<T> = T extends (infer U)[] ? U : never;
type Awaited2<T> = T extends Promise<infer U> ? U : T;
```
Used constantly in library code to derive a return type from a function signature
(`ReturnType<F>`), or a promise's resolved value without the caller re-specifying it.

## 4. `unknown` over `any` at boundaries
Anything from `JSON.parse`, an API response, or `fetch` should be typed `unknown`, then
narrowed with a type guard or a runtime validator before use — `any`
disables checking for everything downstream, `unknown` forces a check:
```ts
function isUser(x: unknown): x is User {
  return typeof x === "object" && x !== null && "id" in x && typeof (x as any).id === "number";
}
```
Hand-written guards like this are exactly where bugs hide (the `as any` inside is
still unchecked) — for anything beyond trivial shapes, a runtime validator (a schema library that parses and returns a typed value) is both the guard and the narrowing in one call, and it's the only thing
that actually checks data arriving from outside the process.

## 5. `satisfies` vs type annotation
```ts
const config = { mode: "dark", retries: 3 } satisfies Config;
```
`satisfies` checks the literal against `Config` without widening its type the way
`: Config` would — `config.mode` stays the literal `"dark"`, not `string`, so
downstream code that needs the literal type (e.g. a switch) still narrows correctly.

## Gotchas
- Narrowing of a `let` variable or parameter used to be lost inside closures; since TS 5.4 it is preserved
  when the variable is not assigned after the closure is created. Where it is still lost, extract to a local
  `const` right after the check.
- `as` casts bypass narrowing entirely and are invisible to `tsc --strict`; look for
  them in review as a signal, not an automatic reject.
- Generic functions with too many type parameters inferred from unrelated arguments
  often mean the function is doing two things — split it.
- Structural typing means two differently-named types with identical shape are
  interchangeable; a discriminant tag is the only way to force distinctness.

## Verify
- [ ] Every union with 2+ variants has a `kind`/`type` discriminant field.
- [ ] Every exhaustive switch over a union has a `never` default branch.
- [ ] No `as any` remains outside a narrow, commented type-guard implementation.
- [ ] External data (API, JSON, env vars) is `unknown` until validated, never typed
      optimistically.

Related: computing-software.software-engineering.typescript.strict-typescript-setup

## Checked
Checked 2026-10-25 against the TypeScript-Website handbook and release notes (TypeScript 6.0 era) and the bundled lib.es5.d.ts. Confirmed: discriminated unions and `never` exhaustiveness checking; type predicates; `K extends keyof T` generic constraints and generic parameter defaults; `infer` in conditional types; `satisfies` validates without changing the expression type (4.9); `JSON.parse` returns `any`; closure narrowing behaviour (5.4 preserves narrowing after the last assignment). Replaced the prose source titles with URLs, rewrote the closure gotcha to match 5.4, and removed the unconfirmed ripgrep pattern and named validator libraries.
Method: documentation only; no commands were run.
