---
id: computing-software.software-engineering.scala.sc-extension-methods-export
name: sc-extension-methods-export
category: computing-software
field: software-engineering
product: scala
tags: [scala, extension-methods-export]
level: advanced
status: docs-checked
description: "Add methods with Scala 3 extension, group them, and forward members with export instead of inheritance."
sources: ["https://docs.scala-lang.org/scala3/reference/contextual/extension-methods.html", "https://docs.scala-lang.org/scala3/reference/other-new-features/export.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension methods and export
- An extension method is available if it is in lexical scope (defined, inherited or imported), in a given instance that is in scope, or in the implicit scope of the receiver type (including a given instance there).
- If `m` is imported by several imports on the same nesting level, the compiler tries each as an extension method and picks the one that type checks, preferring a single non-wildcard import over wildcards; otherwise the reference is ambiguous.
- `export scanUnit.scan` creates alias members for the selected members of a stable path; selectors can be simple, renaming (`x as y`), omitting (`x as _`), `given`, or wildcard `*` (which excludes givens).
- Example from the reference: `export printUnit.{status as _, *}` exports everything except `status`.
Verify: the extension call fails to compile where the extension is not in scope.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 reference pages Extension Methods and Export Clauses. Removed as not confirmed: the one-line `extension (s: String)` example's exact syntax with using clauses and the claim that groups share type parameters.

Method: documentation only; no commands were run.
