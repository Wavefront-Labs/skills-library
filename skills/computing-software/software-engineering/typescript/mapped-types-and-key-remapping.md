---
id: computing-software.software-engineering.typescript.mapped-types-and-key-remapping
name: mapped-types-and-key-remapping
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-types, type-manipulation, mapped-types, keyof, key-remapping, modifiers]
level: practitioner
status: docs-checked
description: "Build mapped types with keyof, modifiers (+/- readonly, ?) and key remapping via as, to generate getters, event maps, form state and filtered object types."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/mapped-types.html
  - https://www.typescriptlang.org/docs/handbook/2/keyof-types.html
  - https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-1.html#key-remapping-in-mapped-types
  - https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type
  - https://github.com/microsoft/TypeScript/wiki/Performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapped types and key remapping

**Goal:** transform object types systematically instead of hand-writing parallel interfaces.

## 1. keyof and indexed access
```ts
interface Settings { theme: "light" | "dark"; fontSize: number; beta: boolean }
type SettingKey = keyof Settings;                 // "theme" | "fontSize" | "beta"
function get<K extends keyof Settings>(k: K): Settings[K] { ... }   // return type follows the key
get("fontSize");                                  // number
```
`keyof` of a type with a string index signature is `string | number`.

## 2. Mapped type basics
```ts
type Flags<T>      = { [K in keyof T]: boolean };
type Mutable<T>    = { -readonly [K in keyof T]: T[K] };
type Concrete<T>   = { [K in keyof T]-?: T[K] };       // remove optional
type Nullable<T>   = { [K in keyof T]: T[K] | null };
```

## 3. Key remapping with `as` (TS 4.1+)
```ts
type Getters<T> = { [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K] };
// { getTheme: () => "light" | "dark"; getFontSize: () => number; getBeta: () => boolean }

type OnlyOfType<T, V> = { [K in keyof T as T[K] extends V ? K : never]: T[K] };
type NumericSettings = OnlyOfType<Settings, number>;      // { fontSize: number }

type EventHandlers<E extends Record<string, unknown>> = {
  [K in keyof E as `on${Capitalize<string & K>}`]?: (payload: E[K]) => void;
};
```
Mapping a key to `never` removes it.

## 4. Practical patterns
Form state from a model:
```ts
type FormState<T> = { [K in keyof T]: { value: T[K]; error?: string; touched: boolean } };
```
Exhaustive lookup tables:
```ts
const labels: { [K in Settings["theme"]]: string } = { light: "Light", dark: "Dark" };   // missing key = error
```
Mapping over a union of keys: `{ [K in "a" | "b"]: number }` same as `Record<"a"|"b", number>`.

## Gotchas
- `string & K` is needed in template literals because `keyof T` may include `number | symbol`.
- Deep recursive mapped types slow the compiler (see the TypeScript performance guide); cap depth or simplify.

## Verify
- Type-level tests (`expectTypeOf<Getters<Settings>>().toEqualTypeOf<...>()`) pass, and renaming a field in `Settings` updates derived keys.

## Checked
Checked 2026-10-25 against the TypeScript-Website handbook and 4.1 release notes. Confirmed: `keyof` of a string index signature giving `string | number`; `-readonly` and `-?` modifiers; key remapping with `as` (4.1) including template literal keys with `Capitalize<string & K>` and filtering by mapping to `never`; `Record<K, T>` equivalent to a mapped type over a key union; expect-type `toEqualTypeOf`. Removed the unconfirmed claims about homomorphic modifier preservation, array/tuple mapping, a quoted compiler error and method-to-property conversion.
Method: documentation only; no commands were run.
