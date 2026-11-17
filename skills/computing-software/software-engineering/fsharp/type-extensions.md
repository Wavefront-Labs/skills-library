---
id: computing-software.software-engineering.fsharp.type-extensions
name: type-extensions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, type-extensions, fsharp-oop, intrinsic-extensions, optional-extensions]
level: practitioner
status: docs-checked
description: "Add members to existing types with intrinsic and optional type extensions."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type extensions
**Goal:** add functionality to types you do not own.

```fsharp
type System.String with                     // optional extension
    member s.Shout() = s.ToUpperInvariant() + "!"

"hi".Shout()

module ListExt =
    type List<'a> with
        member xs.Second = List.tryItem 1 xs

```
- An intrinsic extension extends a user-defined type and is part of the type.
- An optional extension appears outside the original module, namespace or assembly; it is in scope only when its module is opened, is not visible to reflection and cannot be consumed from C# or Visual Basic.

## Gotchas
- Optional extensions must be in modules.

## Self-check
Open the module in one file and confirm `Second` is hidden in files that do not open it.

## Checked
2026-11-03. Confirmed against the Type extensions language-reference page (intrinsic versus optional extensions, scope by opening the module, reflection, C#, modules). Removed: the [<Extension>] C# example, the fields/virtual-members claim and the interface resolution claim.
Method: documentation only; no commands were run.
