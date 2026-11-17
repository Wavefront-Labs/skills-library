---
id: computing-software.software-engineering.groovy.identifiers-keywords
name: identifiers-keywords
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, identifiers-keywords]
level: intro
status: docs-checked
description: "Groovy identifier rules, reserved words, and quoting names with strings (map keys, property access like obj.'a-b')."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/_working-with-collections.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifiers, keywords and quoted names
- Identifiers start with a letter, `$` or `_`; Unicode letters are allowed.
- Reserved keywords (such as `def`, `class`, `default`) cannot in general be variable, field or method names; `as`, `in`, `trait`, `record`, `sealed`, `permits`, `var` and `yields` are only contextual keywords and can be used as names. `const`, `goto`, `strictfp` and `threadsafe` are reserved but unused.
- Quote odd names: `obj.'my-prop'`, `obj."${name}"` (dynamic property name), `map.'a b'`.
- All keywords are valid identifiers after a dot.

## Gotchas
- `map.class` on a `Map` reads the key "class", not the Class object; use `map.getClass()` or `map['class']`.

## Self-check
`def m = [:]; m.in = 1; assert m.in == 1` should pass.

## Checked

2026-11-02. Confirmed against the Syntax chapter (identifiers, keywords list and contextual keywords, quoted identifiers) and Working with collections (map.k reads the key). Removed: the claim that in, as and trait are reserved (they are contextual keywords) and the version hedge.

Method: documentation only; no commands were run.
