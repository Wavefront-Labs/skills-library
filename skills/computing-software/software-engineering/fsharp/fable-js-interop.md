---
id: computing-software.software-engineering.fsharp.fable-js-interop
name: fable-js-interop
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fable-js-interop, fsharp-fable, js-interop, emit-attribute]
level: advanced
status: draft
description: "Call JavaScript from Fable using Emit, import attributes, jsNative and Fable.Core.JsInterop."
sources:
  - https://fable.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fable JS interop
**Goal:** use npm libraries from F#.

```fsharp
open Fable.Core
open Fable.Core.JsInterop

[<Emit("$0 + $1")>]
let addJs (a: int) (b: int) : int = jsNative

[<Import("sum", "lodash")>]
let sum (xs: int[]) : int = jsNative

[<Global>]
let console : obj = jsNative

let el = Browser.Dom.document.getElementById "root"   // needs Fable.Browser.Dom
let o = createObj [ "a" ==> 1; "b" ==> "x" ]
let n : int = o?a
```
- `[<Emit>]` templates inline JS (`$0`, `$1` for arguments).
- `[<Import>]` and `importDefault`/`importAll` bind module exports; `jsNative` is the placeholder body.
- `?` dynamic access and `!!` unsafe cast (from JsInterop) bypass type checking.
- Prefer maintained bindings (Fable.Browser.*, Feliz) to hand-written ones.

## Gotchas
- `[<Emit>]` bodies are not type checked.
- Dynamic access errors appear at runtime in the browser.

## Self-check
Call `addJs 1 2` from a page and confirm 3 in the console.
