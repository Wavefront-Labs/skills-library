---
id: computing-software.software-engineering.fsharp.list-module
name: list-module
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, list-module, fsharp-lists-arrays, fsharp-list, cons-operator]
level: intro
status: docs-checked
description: "Build and transform immutable F# lists with cons, append and the List module functions."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/tour
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lists
**Goal:** use the singly linked immutable list well.

```fsharp
let xs = [ 1; 2; 3 ]
let ys = 0 :: xs               // O(1) cons
let zs = xs @ [ 4; 5 ]         // O(n) append
let [ a; b; c ] = xs           // pattern
let r = [ 1 .. 5 ]             // range
let step = [ 0 .. 2 .. 10 ]    // 0,2,..,10

xs |> List.map (fun x -> x * x)
xs |> List.filter (fun x -> x % 2 = 1)
xs |> List.sum
xs |> List.rev
List.zip [1;2] ["a";"b"]
List.head xs, List.tail xs, List.tryHead [], List.length xs
List.init 3 (fun i -> i * 2)
List.sortBy (fun (n: string) -> n.Length) ["bb";"a"]
List.partition (fun x -> x > 1) xs
List.groupBy (fun x -> x % 2) xs
```
- Linked list: prepend with `::` is O(1); `@` and `List.nth` are O(n).
- Prefer `List.tryHead`/`tryFind`/`tryItem` to throwing variants (`head`, `find`, `item`).

## Gotchas
- `@` is O(n) in the length of the left list; avoid it in a loop.
- `List.head` on an empty list throws; use `List.tryHead`.

## Self-check
`[1;2;3] |> List.map ((+) 1)` is `[2;3;4]`.

## Checked
2026-11-03. Confirmed against the Lists language-reference page (cons O(1), append O(n), List.nth O(n)) and the FSharp.Core ListModule reference (head, tail, tryHead, init, sortBy, partition, groupBy, zip, tryItem, tryFind). Removed: the incomplete-pattern comment, the indexing and arrays advice, and the quadratic-append claim (rewritten to the documented O(n)).
Method: documentation only; no commands were run.
