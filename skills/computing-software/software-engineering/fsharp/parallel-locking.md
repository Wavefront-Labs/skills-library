---
id: computing-software.software-engineering.fsharp.parallel-locking
name: parallel-locking
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, parallel-locking, fsharp-concurrency, lock-function, parallel-for]
level: advanced
status: draft
description: "Run CPU-bound work in parallel with Array.Parallel and Parallel.For, and protect shared state with lock or Interlocked."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallelism and locking
**Goal:** use cores safely.

```fsharp
let squares = [| 1 .. 1000 |] |> Array.Parallel.map (fun x -> x * x)

let counter = ref 0
System.Threading.Tasks.Parallel.For(0, 1000, fun _ -> System.Threading.Interlocked.Increment(&counter.contents) |> ignore) |> ignore

let gate = obj ()
let results = System.Collections.Generic.List<int>()
let add x = lock gate (fun () -> results.Add x)

let cd = System.Collections.Concurrent.ConcurrentDictionary<string,int>()
cd.AddOrUpdate("k", 1, fun _ v -> v + 1) |> ignore

let t = System.Threading.Thread(fun () -> printfn "thread")
t.Start(); t.Join()
```
- `lock obj (fun () -> ...)` is a function in FSharp.Core; locks on reference types only.
- Prefer immutability, `Interlocked`, `ConcurrentDictionary`, channels or MailboxProcessor to explicit locks.
- `Array.Parallel.*` and `PSeq` (third party) parallelise collection operations; measure first, overhead is real.
- Capturing a `let mutable` in a lambda is illegal, so the counter is a ref cell and `Interlocked` takes the address of its `contents` field (unconfirmed on every SDK version; verify it compiles).

## Gotchas
- Never lock on strings or boxed value types.
- Parallelising tiny work items makes things slower.

## Self-check
Run the counter loop and confirm it always reaches 1000.
