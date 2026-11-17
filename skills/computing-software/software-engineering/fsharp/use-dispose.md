---
id: computing-software.software-engineering.fsharp.use-dispose
name: use-dispose
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, use-dispose, fsharp-exceptions, idisposable, use-bang]
level: practitioner
status: docs-checked
description: "Dispose IDisposable resources deterministically with the use binding, use! in task expressions and the using function."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource management
**Goal:** release handles reliably.

```fsharp
let readFirst path =
    use reader = new System.IO.StreamReader(path)    // disposed at end of scope
    reader.ReadLine()

let withUsing path =
    using (new System.IO.StreamReader(path: string)) (fun r -> r.ReadLine())
```
- `use` calls `Dispose` on the value when it goes out of scope; the compiler inserts a null check so `Dispose` is not attempted on null.
- Several `use` bindings are disposed in the reverse order of declaration.
- `using expr (fun value -> ...)` disposes the object when the function returns.
- In `task` expressions `use` binds `IDisposable` or `IAsyncDisposable` values and `use!` disposes at the close of the current scope; since F# 6 `use!` does not allow a null value.

## Gotchas
- A value returned from a `use` scope is disposed before the caller sees it; read what you need inside the scope.

## Self-check
Open a file with `use` inside a function, return, and confirm the file can be deleted afterwards.

## Checked
2026-11-03. Confirmed against the Resource management: the use keyword page (use, using, reverse disposal order, null check) and the Task expressions page (use and use! with IDisposable and IAsyncDisposable, F# 6 null restriction). Removed: the async use! example, the module-top-level claim, FS0760, the tail-call claim and the lazy-seq advice.
Method: documentation only; no commands were run.
