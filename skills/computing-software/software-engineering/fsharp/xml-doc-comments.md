---
id: computing-software.software-engineering.fsharp.xml-doc-comments
name: xml-doc-comments
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, xml-doc-comments, fsharp-docs, triple-slash-comments, generate-documentation-file]
level: intro
status: draft
description: "Document F# APIs with triple-slash XML comments and enable doc generation and validation."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XML documentation
**Goal:** discoverable APIs in IntelliSense and docs.

```fsharp
/// <summary>Adds two numbers.</summary>
/// <param name="a">First value.</param>
/// <param name="b">Second value.</param>
/// <returns>The sum.</returns>
let add (a: int) (b: int) = a + b

/// Plain text is also treated as the summary.
type Point =
    { /// X coordinate
      X: float
      /// Y coordinate
      Y: float }
```
```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <WarnOn>3390</WarnOn>
</PropertyGroup>
```
- `///` comments directly above a declaration attach to it; a plain `///` text without tags is used as the summary.
- `GenerateDocumentationFile` writes `Assembly.xml` that NuGet ships for IntelliSense.
- `--warnon:3390` validates XML doc comments (malformed tags, unknown parameter names).
- Use `<c>`, `<see cref="..."/>`, `<exception cref="...">` tags where useful.
- Regular `//` comments are not doc comments; `(* *)` block comments exist but are rare.

## Gotchas
- A doc comment separated from its declaration by a blank line or attribute order issue may be dropped.
- Generated docs only list public members.

## Self-check
Build with `WarnOn` 3390 and confirm a wrong `param name` produces a warning.
