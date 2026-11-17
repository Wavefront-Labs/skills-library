---
id: computing-software.software-engineering.nim.jsffi-jsobject-dynamic
name: jsffi-jsobject-dynamic
category: computing-software
field: software-engineering
product: nim
tags: [jsffi-jsobject-dynamic, jsffi-and-js-stdlib, jsffi, jsobject, js-dynamic, jsassoc, newjsobject, jsarray, tojs, dot-operator, nim]
level: advanced
status: docs-checked
description: "Use std/jsffi JsObject and JsAssoc for dynamic JS interop with property access, method calls and conversions."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/lib/js/jsffi.nim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jsffi: JsObject and dynamic property access

Goal: call arbitrary JS APIs without writing bindings.

- `import std/jsffi` works only with the JavaScript backend (the module is a fatal error otherwise). `JsObject` is a dynamically typed wrapper around a JS object; `JsAssoc[K, V]` is a statically typed one.
- Create: `newJsObject()`, `newJsAssoc[cstring, int]()`. Keys of a `JsAssoc` must be a `JsKey`: integers, enums, floats or `cstring` (not `string`).
- Properties: `o["key"]` / `o["key"] = v` with a `cstring` or `int` field; the dot accessors `o.a` and `o.a = 20` are experimental (the module uses `{.experimental.}`). Names that are not valid JS identifiers are mangled.
- Read a value back with `o.a.to(int)`; convert a Nim value with `toJs(x)` (a Nim `string` becomes a `cstring`).
- Method calls: `o.method(args)` uses the experimental `.()` operator and returns a `JsObject`, which may be `undefined` when the JS method returns nothing, so be careful.
- Helpers: `jsArguments`, `jsNull`, `jsUndefined`, `isNull`, `isUndefined`, `hasOwnProperty`, `jsTypeOf`, `jsNew` (JS `new`), `jsDelete`, `require`. `JsObject` also overloads operators such as `+`, `-`, `and`, `or`, `not`, `in` and comparisons.
- Global access: `var document {.importc, nodecl.}: JsObject` and `proc jq(selector: JsObject): JsObject {.importjs: "$$(#)".}` for a function.
- Iterate with `pairs`, `items` and `keys` on `JsObject` or `JsAssoc`; build literals of a type with `Type{ a: 1, k: "foo".cstring }`.
- JS error types are wrapped: `JsError`, `JsTypeError`, `JsRangeError` and others.

Gotchas:
- `==` on `JsObject` compares like JavaScript `===`: for real objects that is a comparison of references.
- Misspelled properties are not compile errors; they are `undefined` at runtime.

Verify: reading a property set from JavaScript returns the expected value via `.to(T)`.

## Checked

2026-11-08. Read in full: lib/js/jsffi.nim from nim-lang/Nim (types, JsKey constraint, constructors, conversions, operators, dot and call macros, iterators, `{}` literal macro). Fixed: `newJsAssoc[string, int]` is invalid (use `cstring`); `jsIn` and `jsInstanceOf` do not exist in the module (the `in` operator does). Removed: the int64/BigInt claim and the typed-facade advice (not in the file); manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
