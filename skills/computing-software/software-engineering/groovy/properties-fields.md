---
id: computing-software.software-engineering.groovy.properties-fields
name: properties-fields
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, properties-fields, groovy-classes]
level: practitioner
status: docs-checked
description: "Groovy property syntax (auto getters/setters), fields, access modifiers, and the fact private is not enforced at runtime."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-object-orientation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Properties, fields and access modifiers
- No modifier on a field makes it a property (private field + public getter/setter); `private`/`public`/`protected` declares a plain field.
- Override: define `getX()`/`setX()` yourself; `obj.x` still calls them; `obj.@x` accesses the field directly.
- `final` property: getter only.

## Gotchas
- A `boolean` property has both `isX()` and `getX()`; a `Boolean` property only `getX()`. Inside the class that defines the property, `this.x` accesses the field directly.

## Self-check
`class P { String n }; def p=new P(n:'a'); assert p.getN()=='a'`.

## Checked

2026-11-02. Confirmed against the Object orientation chapter (fields and properties, generated accessors, final, boolean getters, direct access inside the defining class). Removed: default-visibility, dynamic private access and subclass private access claims, and the Boolean/boolean getter error.

Method: documentation only; no commands were run.
