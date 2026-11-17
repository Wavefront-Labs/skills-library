---
id: computing-software.software-engineering.groovy.asboolean-override
name: asboolean-override
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, asboolean-override]
level: advanced
status: docs-checked
description: "Define asBoolean on your classes (or via extension methods) to control Groovy truth."
sources:
  - https://groovy-lang.org/semantics.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom truthiness with asBoolean
```groovy
class Stock { int qty; boolean asBoolean() { qty > 0 } }
assert !new Stock(qty: 0)
assert new Stock(qty: 2)
```
- Implement `asBoolean()` to customise whether Groovy evaluates your object to true or false; Groovy calls it when coercing the object to a boolean.

## Gotchas

## Self-check
Run the snippet; both asserts pass.

## Checked

2026-11-02. Confirmed against the Semantics chapter (Customizing the truth with asBoolean() methods). Removed: the metaClass/extension retrofit claim and the readability advice.

Method: documentation only; no commands were run.
