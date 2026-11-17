---
id: computing-software.software-engineering.fsharp.task-expressions
name: task-expressions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, task-expressions, fsharp-async, task-builder, task-vs-async]
level: practitioner
status: docs-checked
description: "Use the task builder for .NET Tasks and ValueTask and bridge with Async."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# task expressions
**Goal:** write .NET-native async code with minimal overhead.

```fsharp
open System.Threading.Tasks

let readAll (path: string) : Task<string> = task {
    return path
}

let both = task {
    let! a = readAll "a.txt"
    let! b = readAll "b.txt"
    return a + b
}

let a : Async<string> = readAll "a" |> Async.AwaitTask
let t2 : Task<int> = async { return 1 } |> Async.StartAsTask
```
- `task { }` supports `let!`, `use` and `use!` (including `IAsyncDisposable`) and can bind `ValueTask<'T>` and `ValueTask`.
- Task expressions do not take an implicit cancellation token and do not perform implicit cancellation checks; pass a `CancellationToken` yourself.
- Convert a task result to a `ValueTask` with `|> ValueTask<ReturnType>` or `|> ValueTask`.

## Gotchas
- `use!` does not allow a null initial value.

## Self-check
Compile the examples and confirm `readAll "x"` has type `Task<string>`.

## Checked
2026-11-03. Confirmed against the Task expressions language-reference page (let!, use/use!, IAsyncDisposable, ValueTask, cancellation tokens) and the Async expressions page and FSharp.Core Async module reference (AwaitTask, StartAsTask). Removed: the ReadAllTextAsync and WhenAll examples, hot-start and backgroundTask claims, the ASP.NET guidance and the .Result deadlock claim.
Method: documentation only; no commands were run.
