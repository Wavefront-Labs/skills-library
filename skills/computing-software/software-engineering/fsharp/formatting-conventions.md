---
id: computing-software.software-engineering.fsharp.formatting-conventions
name: formatting-conventions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, formatting-conventions, fsharp-style, indentation, offside-rule]
level: intro
status: draft
description: "Format F# with four-space indentation, the offside rule, pipelines and consistent line breaks."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formatting conventions
**Goal:** code that reads uniformly.

```fsharp
let result =
    items
    |> List.filter (fun i -> i.Active)
    |> List.map (fun i -> i.Name)

let veryLongFunctionName
    (firstParameter: int)
    (secondParameter: string)
    : string =
    $"{firstParameter}{secondParameter}"

let r = { Name = "a"; Age = 3 }          // spaces inside braces
let t = (1, 2)                           // space after comma
let f x = x + 1                          // spaces around operators
```
- Use spaces, not tabs; four spaces per indent.
- Whitespace is significant (offside rule): continuation lines must be indented more than the start column of the construct.
- Prefer one pipeline stage per line; keep lines under about 120 characters.
- Place long parameter lists one per line, return type on its own line when wrapping.
- Do not put a space between function name and `(` for method calls: `Console.WriteLine("x")`.

## Gotchas
- Mixed tabs produce error FS1161; configure the editor to insert spaces.
- Moving a `|>` to the end of the previous line is legal but not the convention.

## Self-check
Run `dotnet fantomas --check` on the file and see it pass.
