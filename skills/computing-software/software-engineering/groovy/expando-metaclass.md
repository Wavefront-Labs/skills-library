---
id: computing-software.software-engineering.groovy.expando-metaclass
name: expando-metaclass
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, expando-metaclass]
level: advanced
status: docs-checked
description: "Add methods at runtime with metaClass, ExpandoMetaClass.enableGlobally, and scoped categories (use blocks)."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExpandoMetaClass and categories
```groovy
String.metaClass.shout = { -> delegate.toUpperCase() + '!' }
assert 'hi'.shout() == 'HI!'
class Rev { static String rev(String s) { s.reverse() } }
use(Rev) { assert 'ab'.rev() == 'ba' }
```
- Every class has a `metaClass` property giving an `ExpandoMetaClass`; add methods with `<<` (append; throws if the class already declares the same signature) or `=` (replace).
- By default `ExpandoMetaClass` does not do inheritance; call `ExpandoMetaClass#enableGlobally()` before the app starts to enable it.
- Category methods are static with the receiver as first parameter, active inside the `use` block; `@Category` generates such a class at compile time.

## Gotchas
- Categories are resolved dynamically, so they cannot be used under `@TypeChecked` or `@CompileStatic` (the type checker errors on `use`); an extension module is the type-check-friendly alternative.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (Categories, ExpandoMetaClass: methods and notes). Removed: per-instance metaClass syntax, `removeMetaClass` reset, thread scope, metaClass leakage and Java-call claims.

Method: documentation only; no commands were run.

## Self-check
Run the snippet.
