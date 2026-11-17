---
id: computing-software.software-engineering.groovy.custom-ast-transform
name: custom-ast-transform
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, custom-ast-transform, groovy-compile-meta]
level: sme
status: docs-checked
description: "Implement an AST transformation: annotation plus ASTTransformation, compile phases, and the global transform registration file."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing local and global AST transformations
- Local: define an annotation with `@GroovyASTTransformationClass('pkg.MyXform')`; the transform class implements `ASTTransformation` and has `@GroovyASTTransformation(phase = CompilePhase.SEMANTIC_ANALYSIS)`; `visit(ASTNode[] nodes, SourceUnit source)` modifies the AST.
- Global: list the class name in `META-INF/services/org.codehaus.groovy.transform.ASTTransformation`; its `visit` takes a `SourceUnit` instead of the `ASTNode[]` parameter.

## Gotchas
- Local transformations usually run in the semantic analysis phase. Code injected during or after instruction selection is never visited by the type checker, which breaks `@CompileStatic` users.
- Learn the AST classes (`org.codehaus.groovy.ast`) with the Groovy Console's AST browser tool.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (local and global AST transformations, compile phases, AST browser tip). Removed: separate-compilation, package-rename and menu-path claims.

Method: documentation only; no commands were run.

## Self-check
Inspect a small class in groovyConsole's AST browser to see which phase shows the nodes you need.
