---
id: computing-software.software-engineering.groovy.method-defaults-named-args
name: method-defaults-named-args
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, method-defaults-named-args, groovy-methods]
level: practitioner
status: docs-checked
description: "Default parameter values, named arguments collected in a Map, varargs, and optional parentheses/return."
sources:
  - https://groovy-lang.org/objectorientation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default and named parameters
- Defaults: `def foo(String par1, Integer par2 = 1)` makes `par2` optional (`foo('Marie').age == 1` in the docs example). Parameters are dropped from the right, but mandatory parameters are never dropped: with `def baz(a = 'a', int b, c = 'c', boolean d, e = 'e')`, `baz(42, true) == 'a 42 c true e'`. The same rule applies to constructors.
- Named args: `foo(name: 'Marie', age: 1)` works when the first parameter is a `Map` (`def foo(Map args)`); values are read as `args.name`. With a single `Map` parameter all supplied arguments must be named.
- Mixed named and positional: `def foo(Map args, Integer number)` accepts `foo(name: 'Marie', age: 1, 23)` and `foo(23, name: 'Marie', age: 1)`; named arguments can be in any position and are grouped into the leading Map. The docs advise using this with caution.
- If the Map is not the first parameter, named-argument calls throw `groovy.lang.MissingMethodException`; pass an explicit map instead (`foo(23, [name: 'Marie', age: 1])`).
- Varargs: `def foo(Object... args)` or `Object[] args` as the last parameter. Calling with `null` passes `null` (not a one-element array); calling with an array passes that array.
- Methods always return a value: without `return`, the last evaluated expression is returned.
- Overloads: Groovy picks the most specific method; `foo(Object x)` is preferred over `foo(Object... args)` for a single argument, and non-vararg variants beat vararg ones.

## Gotchas
- Dynamic Groovy dispatches on the runtime types of arguments (multimethods), not declared types; two candidates at equal distance cause an ambiguity runtime exception.

## Self-check
`def f(a, b=2){a+b}; assert f(1)==3 && f(1,5)==6`.

## Checked

Checked 2026-11-09 against groovy-lang.org/objectorientation.html, sections 3.2.1 to 3.2.5 (method definition, named parameters, default arguments, varargs, method selection), read in full.
Confirmed: every point above, including the examples quoted.
Removed as unconfirmed: that defaults generate overloads, the `@NamedParam` claim, optional parentheses and the property-versus-call note, null-target NPE, and the `f(a, b = 1)` plus `f(a)` conflict claim.

Method: documentation only; no commands were run.
