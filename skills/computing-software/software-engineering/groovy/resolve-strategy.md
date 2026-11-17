---
id: computing-software.software-engineering.groovy.resolve-strategy
name: resolve-strategy
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, resolve-strategy]
level: advanced
status: docs-checked
description: "Closure.OWNER_FIRST, DELEGATE_FIRST, OWNER_ONLY, DELEGATE_ONLY, TO_SELF and @DelegatesTo for tooling."
sources:
  - https://groovy-lang.org/closures.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-closures.adoc
  - https://groovy-lang.org/dsl.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-domain-specific-languages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolve strategies for DSLs
```groovy
class Cfg { String name }
def configure(@DelegatesTo(Cfg) Closure c) {
  def cfg = new Cfg(); c.delegate = cfg
  c.resolveStrategy = Closure.DELEGATE_FIRST
  c(); cfg
}
assert configure { name = 'x' }.name == 'x'
```
- `OWNER_FIRST` is the default; `DELEGATE_FIRST` tries the delegate before the owner; `OWNER_ONLY` and `DELEGATE_ONLY` ignore the other side.
- `@DelegatesTo` documents APIs that take closures and gives type information to the static type checker and compiler.

## Gotchas
- With `OWNER_FIRST`, a property or method that exists on the owner is used before the delegate's.

## Self-check
Run the snippet; remove the strategy line and observe the difference when an outer `name` exists.

## Checked

2026-11-02. Confirmed against the Closures chapter (delegation strategies) and the DSL chapter (@DelegatesTo purpose). Removed: the @CompileStatic-specific claims, the strategy/value attribute claim and the outer-variable assignment claim.

Method: documentation only; no commands were run.
