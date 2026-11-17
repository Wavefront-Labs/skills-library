---
id: computing-software.software-engineering.fsharp.map-set
name: map-set
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, map-set, fsharp-sequences-maps, fsharp-map, fsharp-set]
level: practitioner
status: docs-checked
description: "Use immutable Map and Set with the Map and Set modules, understanding the key comparison requirement."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map and Set
**Goal:** pick the right immutable dictionary/set.

```fsharp
let m = Map.ofList [ "a", 1; "b", 2 ]
let m2 = m |> Map.add "c" 3 |> Map.remove "a"
let v = m.["b"]                       // throws if missing
let t = Map.tryFind "z" m             // None
let u = m |> Map.change "b" (Option.map ((+) 1))
let folded = m |> Map.fold (fun acc k v -> acc + v) 0
let keys = m |> Map.toSeq |> Seq.map fst

let s = Set.ofList [ 3; 1; 2; 3 ]     // set [1;2;3]
let union = Set.union s (set [ 9 ])
let sub = Set.isSubset (set [1]) s
let has = s.Contains 2
```
- Keys need the `comparison` constraint.
- `Map.add` of an existing key replaces the value.

## Gotchas
- `m.[k]` throws when the key is missing; use `Map.tryFind`.
- Custom key types must support comparison.

## Self-check
`Map.ofList [1,"a"] |> Map.containsKey 1` is true.

## Checked
2026-11-03. Confirmed against the FSharp.Core MapModule and SetModule references (ofList, add, remove, tryFind, change, fold, toSeq, union, isSubset, containsKey, comparison constraint). Removed: the balanced-tree/O(log n)/sorted-iteration claims, the Dictionary/HashSet/dict advice, KeyNotFoundException naming and the records/unions-comparable claim.
Method: documentation only; no commands were run.
