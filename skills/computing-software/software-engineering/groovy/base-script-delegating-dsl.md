---
id: computing-software.software-engineering.groovy.base-script-delegating-dsl
name: base-script-delegating-dsl
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, base-script-delegating-dsl]
level: sme
status: docs-checked
description: "Run user DSL scripts safely with a custom base Script class, Binding, CompilerConfiguration and import/secure customizers."
sources:
  - https://groovy-lang.org/dsls.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-domain-specific-languages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Base script classes and script DSLs
```groovy
import org.codehaus.groovy.control.CompilerConfiguration
abstract class RulesBase extends Script { def rule(String n, Closure c) { println n } }
def cfg = new CompilerConfiguration(scriptBaseClass: RulesBase.name)
def sh = new GroovyShell(new Binding(), cfg)
sh.evaluate('rule("r1") { }')
```
- `ImportCustomizer` (`org.codehaus.groovy.control.customizers`) adds default imports; `SecureASTCustomizer` restricts the AST with custom `StatementChecker` and `ExpressionChecker` implementations.
- `@BaseScript` on a variable (or with the class as a member) sets the base script class from inside a script.

## Gotchas
- Register customizers on the `CompilerConfiguration` before building the `GroovyShell`; see the compilation customizers section for the full shortcut list.

## Checked

2026-11-02. Confirmed against the Domain-specific languages chapter (base script classes, `@BaseScript`, compilation customizers, `ImportCustomizer`, `SecureASTCustomizer`). Removed: `SandboxTransformer`, the sandboxing advice, package-move and bypass claims.

Method: documentation only; no commands were run.

## Self-check
Run the snippet and confirm "r1" prints.
