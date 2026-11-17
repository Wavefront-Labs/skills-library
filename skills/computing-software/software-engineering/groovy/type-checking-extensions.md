---
id: computing-software.software-engineering.groovy.type-checking-extensions
name: type-checking-extensions
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, type-checking-extensions]
level: sme
status: docs-checked
description: "Customize @TypeChecked/@CompileStatic with extension scripts that handle unresolved properties and methods."
sources:
  - https://groovy-lang.org/semantics.html
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_type-checking-extensions.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type checking extensions
- `@TypeChecked(extensions = ...)` takes an array of extension script names, found on the classpath at compile time; a class name with options (`'com.example.MyChecker(strict: true)'`) is also accepted.
- The script uses event handlers such as `unresolvedVariable`, `methodNotFound`, `afterMethodCall` and `incompatibleAssignment`.
- Set `handled = true` to tell the checker you dealt with the event; `newMethod(...)` declares a method and `makeDynamic(...)` defers the call to runtime.

## Gotchas
- Check the type checking extensions chapter for the exact event list and signatures of the Groovy version in use.

## Checked

2026-11-02. Confirmed against the Type checking extensions chapter (the `extensions` attribute, event table, `handled`, `newMethod`, `makeDynamic`). Removed: the DSL-author claim and the unconfirmed script-compilation advice.

Method: documentation only; no commands were run.

## Self-check
Write an extension marking `unresolvedVariable` named `magic` as `int`, and compile a script using `magic`.
