---
id: computing-software.software-engineering.typescript.function-types-and-overloads
name: function-types-and-overloads
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, function-overloads, typescript-functions, this-parameter, call-signatures, void-return, typescript-types]
level: practitioner
status: docs-checked
description: "Type TypeScript functions precisely: function type expressions, optional/rest params, overload signatures vs unions, this parameters, void vs undefined returns and callbacks."
sources:
  - https://www.typescriptlang.org/docs/handbook/2/functions.html
  - https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
  - https://www.typescriptlang.org/tsconfig/#strictFunctionTypes
  - https://www.typescriptlang.org/tsconfig/#noImplicitThis
  - https://typescript-eslint.io/rules/explicit-module-boundary-types/
  - https://github.com/microsoft/TypeScript/wiki/Performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function types and overloads

**Goal:** function signatures that give callers precise return types and good errors.

## Function types
```ts
type Comparator<T> = (a: T, b: T) => number;
type Handler = { (req: Request): Promise<Response>; displayName?: string };   // call signature + props
type Ctor<T> = new (...args: any[]) => T;                                    // construct signature

function greet(name: string, greeting = "Hello", ...extra: string[]): string { ... }
```
Annotate parameters and exported return types; let locals infer. Explicit return types on
exported functions stop accidental API changes, and the TypeScript performance guide notes that return type annotations can save the compiler work.

## Overloads vs unions
```ts
function parse(input: string): Config;
function parse(input: Buffer, encoding: BufferEncoding): Config;
function parse(input: string | Buffer, encoding?: BufferEncoding): Config {   // implementation, not callable
  ...
}
```
Prefer a union parameter or a generic when the return type doesn't depend on the argument
type (TS handbook "do's and don'ts"): overloads can't be called with a union argument
(`parse(x as string | Buffer)` fails), and the implementation signature is invisible to callers.

Use overloads when the **return type varies** with the input:
```ts
function get(key: "port"): number;
function get(key: "host"): string;
function get(key: string): unknown { ... }
```
(often better as a lookup type: `function get<K extends keyof Settings>(key: K): Settings[K]`).

## this parameters
```ts
interface Button { el: HTMLElement; onClick(this: Button, e: MouseEvent): void }
function handler(this: HTMLElement, ev: Event) { this.classList.toggle("on"); }
```
A fake first parameter checked at compile time, erased at runtime. `noImplicitThis`
flags `this` expressions with an implied `any` type.

## Callbacks and void
```ts
type Listener = (e: Event) => void;
const l: Listener = (e) => 42;           // allowed: callers ignore the return value
function f(): void { return 42; }        // error: declared function must not return a value
```
Don't type callback params as optional just because callers may pass fewer args - passing
fewer is always allowed.

## Gotchas
- `Function` type accepts anything callable with `any` args; use specific signatures.
- Parameter bivariance for methods (`method(x: T): void` syntax) is unsound; with
  `strictFunctionTypes`, property syntax `method: (x: T) => void` is checked contravariantly.
- Generic defaults and constraints on functions: `function first<T = unknown>(xs: readonly T[]): T | undefined`.

## Verify
- [ ] Exported functions have explicit return types (`@typescript-eslint/explicit-module-boundary-types`).
- [ ] Overloads exist only where return types differ by input.

## Checked
Checked 2026-10-25 against the TypeScript-Website handbook (More on Functions, Do's and Don'ts), tsconfig reference, the TypeScript performance wiki and the typescript-eslint rule docs. Confirmed: construct signatures and call signatures; overloads versus union parameters and the implementation signature being invisible; `this` parameters; void-returning callback types; optional parameters in callbacks; strictFunctionTypes applying to function syntax and not method syntax; the explicit-module-boundary-types rule exists. Reworded the claim that `noImplicitThis` is part of strict (membership is not stated on the option page).
Method: documentation only; no commands were run.
