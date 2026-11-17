---
id: computing-software.software-engineering.groovy.macro-methods
name: macro-methods
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, macro-methods]
level: sme
status: docs-checked
description: "Construct AST fragments with AstBuilder, and in Groovy 3+ with macro methods (org.apache.groovy.macrolib)."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AST builders and macro methods
- `macro` turns plain code in a closure into AST nodes (for example a `ReturnStatement`). Signatures: `macro(Closure)`, `macro(Boolean, Closure)` (true wraps expressions in a statement, false returns an expression), `macro(CompilePhase, Closure)` and `macro(CompilePhase, Boolean, Closure)`.
- `GeneralUtils` (`org.codehaus.groovy.ast.tool`) static methods such as `varX` ease building nodes by hand; `ASTMatcher` filters nodes by pattern.

## Gotchas
- The `macro` signatures are in `org.codehaus.groovy.macro.runtime.MacroGroovyMethods`.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (Macro methods, ASTMatcher). Removed: `AstBuilder` method names (not in the chapter), `ClassNodeUtils`, `callX`, the `groovy-macro` requirement and package-rename claims.

Method: documentation only; no commands were run.

## Self-check
Use `macro { return 42 }` in a local AST transform to add a method to a class and call it.
