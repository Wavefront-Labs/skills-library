---
id: computing-software.software-engineering.groovy.dynamic-methods-missing
name: dynamic-methods-missing
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, dynamic-methods-missing, groovy-mop]
level: advanced
status: docs-checked
description: "Intercept unknown method and property calls with methodMissing, propertyMissing, GroovyInterceptable and invokeMethod."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# methodMissing, propertyMissing, invokeMethod
```groovy
class Dyn {
  def methodMissing(String name, args) { "called $name${args.toList()}" }
  def propertyMissing(String name) { "prop $name" }
}
assert new Dyn().foo(1) == 'called foo[1]' && new Dyn().bar == 'prop bar'
```
- `methodMissing` is invoked only when no method is found; using `invokeMethod` to intercept missing methods is discouraged.
- Implement `GroovyInterceptable` (marker interface) to route every call through `invokeMethod`; default methods such as `println` are injected into all objects, so they are intercepted too.
- To intercept all calls without the interface, implement `invokeMethod` on the object's `MetaClass` (works for POGOs and POJOs).
- `propertyMissing(String)` handles failing getter lookups; add `propertyMissing(String, value)` for setters.

## Gotchas
- Register the method on the `ExpandoMetaClass` the first time `methodMissing` resolves it, so later calls avoid the overhead.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (methodMissing, propertyMissing, GroovyInterceptable, invokeMethod). Removed: the `getProperty`/`setProperty` line, the recursion tip and the `@CompileStatic` claim.

Method: documentation only; no commands were run.

## Self-check
Run the snippet.
