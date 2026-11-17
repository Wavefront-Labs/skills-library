---
id: computing-software.software-engineering.typescript.utility-types
name: utility-types
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-types, type-manipulation, utility-types, partial, pick, omit, record, returntype]
level: practitioner
status: docs-checked
description: "Derive types instead of duplicating them with TypeScript's built-in utility types: Partial, Required, Pick, Omit, Record, ReturnType, Awaited, NonNullable and friends."
sources:
  - https://www.typescriptlang.org/docs/handbook/utility-types.html
  - https://www.typescriptlang.org/docs/handbook/2/types-from-types.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html#the-noinfer-utility-type
  - https://www.typescriptlang.org/tsconfig/#noUncheckedIndexedAccess
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypeScript utility types

**Goal:** one source of truth per shape; related types (inputs, patches, views) derived so they cannot drift.

## 1. The everyday set
```ts
interface User { id: string; email: string; name: string; role: "admin" | "member"; createdAt: Date }

type NewUser    = Omit<User, "id" | "createdAt">;        // create payload
type UserPatch  = Partial<Pick<User, "email" | "name">>;  // PATCH body
type UserView   = Readonly<Pick<User, "id" | "name">>;
type ById       = Record<User["id"], User>;               // { [id: string]: User }
type Complete   = Required<UserPatch>;
type Role       = User["role"];                           // indexed access
```

## 2. Function-derived types
```ts
async function loadUser(id: string, opts?: { cache: boolean }) { /* ... */ return user; }
type LoadArgs   = Parameters<typeof loadUser>;            // [id: string, opts?: {...}]
type Loaded     = Awaited<ReturnType<typeof loadUser>>;   // User (unwraps Promise)
class Repo { constructor(db: Db, log: Logger) {} }
type RepoDeps   = ConstructorParameters<typeof Repo>;
type RepoT      = InstanceType<typeof Repo>;
```
Useful for typing wrappers around third-party functions whose types are not exported.

## 3. Union utilities
```ts
type Status = "draft" | "active" | "archived" | null;
type Live    = Exclude<Status, "archived" | null>;        // "draft" | "active"
type Ended   = Extract<Status, "archived">;
type Present = NonNullable<Status>;
```

## 4. Literal-preserving helpers
- `NoInfer<T>` (TS 5.4) stops a parameter from influencing inference: `function pick<T extends string>(all: T[], d: NoInfer<T>)`.
- `as const` + `typeof` to derive unions from runtime values:
```ts
const ROLES = ["admin", "member", "guest"] as const;
type RoleName = (typeof ROLES)[number];
```
- `satisfies` checks a value against a type without widening it: `const routes = { home: "/" } satisfies Record<string, string>;`

## Gotchas
- `Omit<T, K>` does not check that `K` exists in `T` (typos compile). A stricter alias: `type StrictOmit<T, K extends keyof T> = Omit<T, K>`.
- `Omit`/`Pick` on a union type distribute poorly (keys common to all members only); write a distributive version `T extends unknown ? Omit<T, K> : never`.
- `Partial` is shallow; deep partials need a recursive mapped type, and are usually a sign the API should accept a narrower type.
- `Record<string, T>` claims every key exists; with `noUncheckedIndexedAccess` indexing yields `T | undefined`, which is the honest type.

## Verify
- Change a field in the base interface and confirm every derived type and its usages update or error at compile time (`tsc --noEmit`).

## Checked
Checked 2026-10-25 against the TypeScript-Website Utility Types reference and the bundled lib.es5.d.ts. Confirmed: Partial, Required, Readonly, Pick, Omit, Record, Exclude, Extract, NonNullable, Parameters, ConstructorParameters, ReturnType, InstanceType and Awaited (4.5) exist as described; `NoInfer` (5.4); `Omit<T, K extends keyof any>` does not require K to be a key of T; `satisfies` (4.9); noUncheckedIndexedAccess adds undefined. Removed the unconfirmed `Expand` prettifier remark.
Method: documentation only; no commands were run.
