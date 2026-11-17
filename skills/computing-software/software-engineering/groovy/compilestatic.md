---
id: computing-software.software-engineering.groovy.compilestatic
name: compilestatic
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, compilestatic]
level: advanced
status: docs-checked
description: "@CompileStatic generates Java-like bytecode: faster, no metaClass lookups, with semantics changes around dispatch and dynamic features."
sources:
  - https://groovy-lang.org/semantics.html
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/tools-groovyc.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @CompileStatic and performance
- Add `@groovy.transform.CompileStatic` to class or method; `@CompileDynamic` opts a method back out.
- `@CompileStatic` activates static compilation; a `@CompileDynamic` method opts out of static compilation (see the type checking section of the Semantics chapter for the exact rules).
- Categories (`use`) are resolved dynamically, so they cannot be used under `@CompileStatic`.
- `groovyc -d <dir>` sets where class files are placed, so you can inspect the output with `javap -c`.

## Gotchas
- Benchmark before widespread use; there is no universal speedup figure.

## Checked

2026-11-02. Confirmed against the Semantics chapter (`@CompileDynamic` note), the Metaprogramming chapter (`@CompileStatic`, categories note) and the groovyc page (`-d`). Removed: MOP-bypass wording, usage recommendations, multimethod and duck-typing claims.

Method: documentation only; no commands were run.

## Self-check
Compile a class with and without `@CompileStatic` and compare `javap` output for `invokedynamic` or call sites.
