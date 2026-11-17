---
id: computing-software.software-engineering.typescript.branded-types-and-enums-vs-unions
name: branded-types-and-enums-vs-unions
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-types, branded-types, nominal-typing, typescript-enums, string-literal-unions, const-enum]
level: practitioner
status: verified
description: "Add nominal safety to structural TypeScript with branded types for IDs and units, and choose between enums, const objects and literal unions."
sources:
  - https://www.typescriptlang.org/docs/handbook/enums.html
  - https://www.typescriptlang.org/docs/handbook/type-compatibility.html
  - https://www.typescriptlang.org/tsconfig/#erasableSyntaxOnly
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branded types and enums vs unions

**Goal:** stop mixing up structurally identical values (UserId vs OrderId, cents vs euros) and choose the right construct for fixed sets of values.

## 1. Branded (nominal) types
```ts
declare const brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [brand]: B };

type UserId  = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Cents   = Brand<number, "Cents">;

const UserId = (s: string): UserId => {
  if (!/^usr_[a-z0-9]{12}$/.test(s)) throw new Error(`bad user id: ${s}`);
  return s as UserId;
};
function getOrder(id: OrderId) {}
getOrder(UserId("usr_abc123def456"));   // compile error
```
Brands exist only at compile time (zero runtime cost). Create them only in validating constructors or parsers (Zod `.brand<"UserId">()`), so a branded value means "validated".

## 2. Enums: what they compile to
```ts
enum Status { Draft = "draft", Active = "active" }   // emits a runtime object
const enum Dir { Up, Down }                          // inlined; AMBIENT (.d.ts) const enums break isolatedModules consumers
enum Num { A, B }                                     // numeric: reverse mapping; any `number` variable is still assignable
```
Problems: emit runtime code (not erasable; Node's type stripping and `erasableSyntaxOnly` reject them), numeric enums are loosely typed (since TS 5.0 an out-of-domain numeric literal like `const n: Num = 42` errors, but a plain `number` value is still accepted), and enums are nominal so `"draft"` literal does not satisfy `Status`.

## 3. Prefer literal unions, or a const object when you need values at runtime
```ts
type Status = "draft" | "active" | "archived";

const Status = { Draft: "draft", Active: "active", Archived: "archived" } as const;
type Status = (typeof Status)[keyof typeof Status];
Object.values(Status);                       // iterate at runtime
function set(s: Status) {}  set("draft");    // plain literals accepted
```

## 4. Exhaustiveness
```ts
function label(s: Status): string {
  switch (s) {
    case "draft": return "Draft";
    case "active": return "Active";
    case "archived": return "Archived";
    default: { const never: never = s; throw new Error(`unhandled ${never}`); }
  }
}
```
Adding a member makes the `never` assignment fail to compile at every switch.

## Gotchas
- Branded values are still their base type: `userId.toUpperCase()` returns plain `string`, dropping the brand.
- Serialisation strips nothing (brands are types only), but deserialised JSON must be re-validated to regain brands.
- Ambient `const enum` (in published `.d.ts` files) is incompatible with consumers using `isolatedModules`; the handbook says this pitfall applies to ambient const enums only. Avoid them in libraries.

## Verify
- `@ts-expect-error` tests confirm cross-brand assignment fails, and `tsc --erasableSyntaxOnly` (TS 5.8) passes if you run TS directly in Node.
