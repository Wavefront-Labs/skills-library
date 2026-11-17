---
id: computing-software.software-engineering.fsharp.async-workflows
name: async-workflows
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, async-workflows, fsharp-async, async-parallel, cancellation-token]
level: practitioner
status: draft
description: "Compose F# async workflows, run them in parallel, start them and cancel with CancellationToken."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# async workflows
**Goal:** write cold, composable asynchronous code.

```fsharp
let fetch (url: string) = async {
    use client = new System.Net.Http.HttpClient()
    let! body = client.GetStringAsync url |> Async.AwaitTask
    return body.Length
}

let sizes =
    [ "https://example.com"; "https://example.org" ]
    |> List.map fetch
    |> Async.Parallel            // Async<int[]>
    |> Async.RunSynchronously    // blocks: use only at program edges

let work = async { do! Async.Sleep 1000; return 1 }
use cts = new System.Threading.CancellationTokenSource()
Async.Start(work, cts.Token)
cts.Cancel()
let child = async { let! t = Async.StartChild work in return! t }
```
- `Async<'T>` is a cold description; nothing runs until `Async.RunSynchronously`, `Async.Start` or `Async.StartAsTask`.
- `Async.Parallel` runs a sequence concurrently (optional `maxDegreeOfParallelism` in newer FSharp.Core); `Async.Sequential` runs one by one.
- `async` carries an implicit cancellation token; `Async.CancellationToken` reads it, `Async.TryCancelled` handles cancellation.
- `Async.AwaitTask` / `Async.StartAsTask` interoperate with `Task`.

## Gotchas
- `Async.RunSynchronously` on a UI or ASP.NET sync context can deadlock.
- Exceptions in `Async.Start` are unobserved unless handled; wrap with `Async.Catch`.

## Self-check
Parallel-map three `Async.Sleep 1000` workflows and confirm total time near 1s.
