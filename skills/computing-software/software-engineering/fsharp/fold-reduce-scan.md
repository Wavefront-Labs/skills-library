---
id: computing-software.software-engineering.fsharp.fold-reduce-scan
name: fold-reduce-scan
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fold-reduce-scan, fsharp-sequences-maps, fold, reduce, collect-bind]
level: practitioner
status: docs-checked
description: "Aggregate collections with fold, reduce, scan, collect and choose, knowing which handle empty input."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folding and aggregation
**Goal:** replace loops with folds.

```fsharp
[1;2;3] |> List.fold (fun acc x -> acc + x) 0         // 6
[1;2;3] |> List.reduce max                             // 3; throws on empty
[1;2;3] |> List.scan (+) 0                             // [0;1;3;6]
[1;2;3] |> List.foldBack (fun x acc -> x :: acc) []    // right fold
[ [1;2]; [3] ] |> List.collect id                      // flatten
[ Some 1; None; Some 3 ] |> List.choose id             // [1;3]
[1;2;3;4] |> List.partition (fun x -> x < 3)
[1;2;3;4] |> List.pairwise
["a";"b"] |> List.mapi (fun i s -> i, s)
[1;2;3] |> List.exists ((=) 2) , List.forall (fun x -> x > 0) [1;2]
[3;1;2] |> List.sortDescending |> List.truncate 2
```
- `fold` takes an initial state, so an empty list just returns that state; `List.reduce` throws on an empty list.
- `choose` applies a function returning an option and keeps the `Some` values; `collect` maps and concatenates.
- The same functions exist on the `Array` and `Seq` modules.

## Gotchas
- `List.average` throws on an empty list.
- Parameter order for fold: folder, state, list; with a pipe it reads `xs |> List.fold f init`.

## Self-check
`List.fold (+) 0 []` is 0 and `List.reduce (+) []` throws.

## Checked
2026-11-03. Confirmed against the FSharp.Core ListModule reference (fold, reduce, scan, foldBack, collect, choose, partition, pairwise, mapi, exists, forall, sortDescending, truncate, average throwing on an empty list). Removed: the Split and Int32.TryParse examples, the max/min exception claim, the foldBack laziness claim and the List.sum empty claim.
Method: documentation only; no commands were run.
