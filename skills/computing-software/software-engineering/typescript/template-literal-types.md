---
id: computing-software.software-engineering.typescript.template-literal-types
name: template-literal-types
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-types, type-manipulation, template-literal-types, string-manipulation-types, infer]
level: practitioner
status: gated
description: "Use template literal types to type string formats: route params, event names, CSS units and IDs, with intrinsic string helpers and infer-based parsing."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html
  - https://www.typescriptlang.org/docs/handbook/2/conditional-types.html#inferring-within-conditional-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template literal types

**Goal:** catch malformed strings (event names, routes, keys) at compile time and extract typed data from string patterns.

## 1. Building string unions
```ts
type Entity = "user" | "order";
type Action = "created" | "deleted";
type EventName = `${Entity}.${Action}`;          // "user.created" | "user.deleted" | "order.created" | "order.deleted"
type CssLength = `${number}${"px" | "rem" | "%"}`;
const w: CssLength = "12px";                     // ok; "12-px" and "px" are errors (but "12 px" is accepted, see Gotchas)
type OrderId = `ord_${string}`;
```
Intrinsics: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`.

## 2. Parsing with infer
```ts
type RouteParams<P extends string> =
  P extends `${string}:${infer Param}/${infer Rest}` ? { [K in Param | keyof RouteParams<Rest>]: string } :
  P extends `${string}:${infer Param}` ? { [K in Param]: string } :
  {};
function route<P extends string>(path: P, handler: (params: RouteParams<P>) => void) {}
route("/users/:userId/orders/:orderId", p => p.orderId);   // p: { userId: string; orderId: string }
```
Express, Hono and TanStack Router use this technique (gated: unconfirmed, source is paywalled or blocked).

## 3. Typed event emitters
```ts
type Events = { "user.created": { id: string }; "order.paid": { id: string; amount: number } };
declare function on<E extends keyof Events>(name: E, fn: (p: Events[E]) => void): void;
on("order.paid", p => p.amount);      // typed payload; misspelled event names fail
```

## 4. Key transforms
```ts
type SnakeToCamel<S extends string> =
  S extends `${infer H}_${infer T}` ? `${H}${Capitalize<SnakeToCamel<T>>}` : S;
type T1 = SnakeToCamel<"created_at_utc">;    // "createdAtUtc"
```

## Gotchas
- Cross-product unions explode: three unions of 50 members yield 125,000 members and slow or crash the checker (a union of 100,000 members already fails with TS2590 "union type that is too complex", checked on TypeScript 5.9.3 and 7.0.2). Keep combinations small.
- `${number}` accepts any string that parses as a finite number, including `"1e3"`, `"0x10"`, `"+5"`, `" 12"` and `"12 "` (so `${number}px` accepts `"12 px"`); it rejects `""`, `"Infinity"`, `"1_0"` and `"abc"` (checked on TypeScript 5.9.3 and 7.0.2). Do not rely on it for strict validation.
- Recursion depth is limited: a tail-recursive string builder worked at 900 iterations and failed with TS2589 at 1100 (checked); non-tail recursion hits the limit sooner.
- Compile-time types do not validate runtime input: strings from JSON/URLs still need runtime parsing (Zod `z.templateLiteral`, regex).

## Verify
- `// @ts-expect-error` lines with invalid event names or routes compile only while the error is present; `tsc --noEmit` passes.
