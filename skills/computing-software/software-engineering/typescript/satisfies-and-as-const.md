---
id: computing-software.software-engineering.typescript.satisfies-and-as-const
name: satisfies-and-as-const
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, satisfies-operator, as-const, literal-types, type-assertions, const-type-parameters, typescript-types]
level: practitioner
status: verified
description: "Get precise literal types without losing checking: as const, the satisfies operator vs annotations vs as assertions, const type parameters, and deriving unions from values."
sources: ["https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator", "https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#const-assertions", "https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html#const-type-parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# satisfies and as const

**Goal:** config objects and lookup tables that are both validated against a type and
keep their exact literal types.

## The three ways to attach a type
```ts
type Route = { path: string; auth: boolean };

const a: Record<string, Route> = { home: { path: "/", auth: false } };
a.home;        // ok... but a.typo is also "ok" (Record<string, ...>) and keys are lost

const b = { home: { path: "/", auth: false } } as Record<string, Route>;   // assertion: no checking of extra/missing

const c = {
  home: { path: "/", auth: false },
  admin: { path: "/admin", auth: true },
} satisfies Record<string, Route>;
c.admin;       // ok, keys preserved: "home" | "admin"
c.typo;        // error
```
`satisfies` checks the value against the type but keeps the **inferred** type of the
expression. Annotation (`:`) widens to the annotated type. `as` asserts and should be rare.

## as const
```ts
const ROLES = ["admin", "editor", "viewer"] as const;    // readonly ["admin", "editor", "viewer"]
type Role = (typeof ROLES)[number];                      // "admin" | "editor" | "viewer"

const STATUS = { Active: "active", Banned: "banned" } as const;
type Status = (typeof STATUS)[keyof typeof STATUS];      // "active" | "banned"
```
Values become readonly and literal-typed - a single source of truth for both runtime lists
(dropdowns, validation) and compile-time unions. A lighter alternative to `enum`.

## Combine them
```ts
const routes = {
  home: { path: "/", auth: false },
  admin: { path: "/admin", auth: true },
} as const satisfies Record<string, Route>;
routes.admin.path;    // type "/admin"
```

## const type parameters (TS 5.0; all examples here type-checked on TypeScript 5.9.3 and 7.0.2)
```ts
function defineRoutes<const T extends Record<string, Route>>(r: T): T { return r; }
const r = defineRoutes({ home: { path: "/", auth: false } });   // literal types inferred without `as const` at call site
```
Great for library helpers (`defineConfig`).

## When `as` is legitimate
DOM queries (`document.getElementById("x") as HTMLCanvasElement` after you know it), test
fixtures, and narrowing results the compiler cannot follow. Never `as unknown as T` to silence a
real mismatch - fix the type or validate at runtime.

## Verify
- [ ] Config tables use `satisfies` (checked + precise), not `as`.
- [ ] Unions duplicated as string arrays are derived from one `as const` source.
