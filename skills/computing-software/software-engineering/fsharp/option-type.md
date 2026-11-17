---
id: computing-software.software-engineering.fsharp.option-type
name: option-type
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, option-type, fsharp-option-result, option-module, null-safety]
level: intro
status: docs-checked
description: "Represent missing values with option and compose with Option.map, bind, defaultValue and the Option module instead of null."
sources:
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/option.fsi
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/map.fsi
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Option
**Goal:** replace null with `option`.

```fsharp
let find k m = Map.tryFind k m                  // returns 'v option
let len = Some "abc" |> Option.map String.length        // Some 3
let r = Some 3 |> Option.bind (fun x -> if x > 2 then Some (x * 2) else None)
let v = None |> Option.defaultValue 0           // 0
let w = Option.defaultWith (fun () -> expensive ()) None
let isOk = Option.isSome (Some 1)
let both = Option.map2 (+) (Some 1) (Some 2)    // Some 3
let flat = Option.toList (Some 1)
let fromNull = Option.ofObj (null: string)      // None
match Some 5 with
| Some n when n > 3 -> "big"
| Some _ | None -> "small or none"
```
- The `Option` module has `map`, `bind`, `filter`, `orElse`, `defaultValue`, `iter`, `count`, `toArray`, `ofObj` and `toObj`.
- `Option.get` and `Option.defaultValue` are both in the module.
- Nullable: `Option.ofNullable`/`Option.toNullable` bridge to `System.Nullable`.

## Self-check
`None |> Option.map ((+) 1)` is `None`.

## Checked
2026-11-02. Confirmed against FSharp.Core option.fsi (dotnet/fsharp main): defaultValue, defaultWith, orElse, get, count, iter, map, map2, bind, filter, toArray, toList, ofNullable, toNullable, ofObj, toObj, isSome, toValueOption; Map.tryFind returns an option (map.fsi). Removed: the advice to prefer pattern matching over Option.get and not to use option for errors, the claim that Option.get throws on None (not in the source read), the 'Some null' gotcha and the sentence on where the module lives.
Method: documentation only; no commands were run.
