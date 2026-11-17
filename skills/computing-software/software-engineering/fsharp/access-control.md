---
id: computing-software.software-engineering.fsharp.access-control
name: access-control
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, access-control, fsharp-modules, fsi-signature-files, private-internal]
level: practitioner
status: docs-checked
description: "Control visibility with public, internal and private and hide implementation with .fsi signature files."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessibility and signature files
**Goal:** expose a minimal API.

```fsharp
module Lib =
    let publicFn x = x + 1
    let internal internalFn x = x
    let private privateFn x = x
```
Signature file `Lib.fsi` next to `Lib.fs`:
```fsharp
module Lib
val publicFn: int -> int
```
- Access specifiers `public`, `internal` and `private` apply to modules, types, methods, values, functions, properties and explicit fields. `public` is accessible to all callers, `internal` only from the same assembly, `private` only from the enclosing type or module.
- If no specifier is used the default is `public`, except for `let` bindings in a type, which are always private to the type.
- A signature file lists the public signatures of a set of program elements and can specify accessibility; it should precede the associated code file in the project. Accessibility modifiers in the signature must match those in the implementation.
- Records and discriminated unions must expose either all or none of their fields and constructors in a signature, and the order must match the implementation.

## Gotchas
- A signature file must match the implementation (modifiers, order of fields).

## Self-check
Add an `.fsi` omitting a function and confirm another project cannot call it.
## Checked
2026-11-02. Confirmed against Microsoft Learn "Access Control" and "Signatures" (F# language reference). Removed: the private-constructor and internal-record samples, `InternalsVisibleTo`, the FS0034 error code and the private-type-in-signature claim.
Method: documentation only; no commands were run.
