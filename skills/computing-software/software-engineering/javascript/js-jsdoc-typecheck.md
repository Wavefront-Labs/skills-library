---
id: computing-software.software-engineering.javascript.js-jsdoc-typecheck
name: js-jsdoc-typecheck
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, jsdoc-typecheck, js-ts-interop]
level: practitioner
status: docs-checked
description: "Annotate plain JavaScript with TypeScript-supported JSDoc tags: @type, @param, @returns, @typedef, @template, @import and casts."
sources: ["https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSDoc types with checkJs

- The supported tags (TypeScript JSDoc Reference): `@type`, `@import`, `@param` (`@arg`, `@argument`), `@returns` (`@return`), `@typedef`, `@callback`, `@template`, `@satisfies`; class tags `@public`, `@private`, `@protected`, `@readonly`, `@override`, `@extends`, `@implements`, `@class`, `@this`; and documentation tags `@deprecated`, `@see`, `@link`, plus `@enum` and `@author`.
- Any tag not listed (for example `@async`) is not yet supported. Only the documentation tags are supported in TypeScript files; the rest apply to JavaScript files.
- `@type` accepts primitives, types from TypeScript declarations (global or imported), and `@typedef` types. Most JSDoc syntax and any TypeScript syntax works: unions (`string | boolean`), arrays (`number[]`, `Array<number>`), object literals (`{ a: string, b: number }`), map-like objects (`Object.<string, number>`), and functions (`(s: string, b: boolean) => number` or Closure `function(string, boolean): number`).
- `@param {string} [p3]` marks an optional parameter (also `{string=}`), `[p4="test"]` gives a default; nested object fields are written `options.prop1`.
- `@typedef` defines named types (a single-line TypeScript form also works); `@callback` defines a function type; `@template T` declares generics.
- Import other files' types with `import("./types").Pet` or the `@import {Pet} from "./types"` tag.
- Casts: put a `@type` tag before a parenthesized expression, for example `/** @type {number} */ (numberOrString)`; `/** @type {const} */(1)` casts to const.
- Enabling checking (`// @ts-check`, `checkJs`) and suppression comments are in the TypeScript Handbook "Type Checking JavaScript Files" page, not this reference; confirm there before relying on them.

Self-check: annotate a function with `@param {string} name` and call it with a number; the editor or compiler flags it.

## Checked

2026-11-08. Confirmed on the TypeScript JSDoc Reference: the tag list, unsupported-tag note, `@type`, `@param`/`@returns` optional-parameter syntax, `@typedef`, `@callback`, `@template`, `@import`, and cast syntax. Removed the `tsc --noEmit -p .` CI recipe, `// @ts-check` and `checkJs` configuration, `@ts-expect-error` versus `@ts-ignore`, and `declaration`/`emitDeclarationOnly` publishing advice, none of which this page states.

Method: docs-only read of cited pages, 2026-11-08
