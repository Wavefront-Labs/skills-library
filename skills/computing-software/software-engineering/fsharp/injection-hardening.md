---
id: computing-software.software-engineering.fsharp.injection-hardening
name: injection-hardening
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, injection-hardening, fsharp-security, input-validation, sql-injection]
level: advanced
status: draft
description: "Harden F# services against SQL injection, unsafe deserialisation, path traversal and regex DoS."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input hardening
**Goal:** treat all external input as untrusted.

```fsharp
// parameterised SQL (never interpolate)
conn.Execute("SELECT * FROM T WHERE Name = @n", {| n = userInput |})

// path traversal check
let safeCombine (root: string) (rel: string) =
    let full = System.IO.Path.GetFullPath(System.IO.Path.Combine(root, rel))
    if full.StartsWith(System.IO.Path.GetFullPath root, System.StringComparison.Ordinal)
    then Ok full else Error "outside root"

// regex timeout
let rx = System.Text.RegularExpressions.Regex(@"^\w+$", System.Text.RegularExpressions.RegexOptions.None, System.TimeSpan.FromMilliseconds 100.)

// smart constructors validate once
type Email = private Email of string
```
- Use parameterised queries; F# `$"..."` interpolation into SQL is still string concatenation.
- Do not use `BinaryFormatter` or other type-polymorphic deserialisers on untrusted data; use `System.Text.Json` with concrete types.
- Validate at the boundary into domain types (single-case unions, `Result`); trust inside.
- Set request body limits and timeouts at the web server.
- Escape output for the target context (HTML encoders); Giraffe's view engine encodes by default.

## Gotchas
- `StartsWith` checks must compare normalised full paths with a trailing separator to avoid sibling-prefix bypasses (`/data` vs `/data2`).
- Do not log raw user input unsanitised.

## Self-check
Call `safeCombine "root" "../x"` and confirm `Error`.
