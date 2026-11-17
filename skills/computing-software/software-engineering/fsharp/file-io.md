---
id: computing-software.software-engineering.fsharp.file-io
name: file-io
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, file-io, fsharp-io, system-io, file-readlines]
level: practitioner
status: draft
description: "Read and write files and directories using System.IO with use bindings, ReadLines and async stream APIs from F#."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File I/O
**Goal:** do file work safely with System.IO.

```fsharp
open System.IO

let text = File.ReadAllText "in.txt"
File.WriteAllText("out.txt", "hello")
File.AppendAllLines("log.txt", [ "line" ])
let lines = File.ReadLines "big.txt" |> Seq.filter (fun l -> l.Contains "ERR") |> Seq.toList

let copyUpper src dst =
    use r = new StreamReader(src)
    use w = new StreamWriter(dst)
    while not r.EndOfStream do
        w.WriteLine(r.ReadLine().ToUpperInvariant())

let files = Directory.EnumerateFiles("dir", "*.fs", SearchOption.AllDirectories)
let p = Path.Combine("a", "b", "c.txt")
let ext = Path.GetExtension p
let exists = File.Exists p
let readAsync path = task { return! File.ReadAllTextAsync path }
```
- `File.ReadLines` is lazy; `ReadAllLines` loads everything.
- `Path.Combine` handles separators; never concatenate with a hard-coded slash.
- Use `FileStream` with `FileOptions.Asynchronous` and `useAsync` for large async work.
- Specify encoding when it matters: `File.ReadAllText(p, System.Text.Encoding.UTF8)`.

## Gotchas
- Not disposing writers loses buffered data.
- Relative paths resolve against the process working directory, not the executable.

## Self-check
Write then read a temp file and compare the contents.
