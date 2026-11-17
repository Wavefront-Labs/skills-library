---
id: computing-software.software-engineering.javascript.js-private-methods-brand-checks
name: js-private-methods-brand-checks
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, private-in-check, js-class-fields]
level: advanced
status: docs-checked
description: "Use #private fields and methods, the #x in obj brand check, and know their limits with subclasses and proxies."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_elements", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private methods and brand checks

- `#priv` fields and methods are created with a hash prefix and enforced by JavaScript itself: they can be accessed only with dot notation inside the class that declares them. Referring to a `#name` outside the class, to an undeclared private name, or using `delete` on one is a syntax error.
- Brand check: `#x in obj` tests whether an object has the private element, e.g. `static has(o) { return #x in o; }` (MDN shows `if (#x in obj) return obj.#x;`).
- A subclass cannot access a base class's private field: `#privateField` is private to the class that declares it.
- Private fields are added before the constructor runs in a base class, or immediately after `super()` returns in a subclass.
- Private static fields and methods can be accessed only by the class that defines them; call them through the class name, not `this`, or `Subclass.method()` throws `TypeError`.
- A `Proxy` around an instance has no access to the original's private elements: forward calls with the original object as `this`.

Self-check: `class A { #x = 1; static has(o) { return #x in o; } }` then `A.has(new A())` is true and `A.has({})` is false.

## Checked

Date: 2026-11-03. Confirmed on MDN Classes/Private_elements (syntax-error rules, `#x in obj`, subclass note, initialisation timing, private static restriction) and Global_Objects/Proxy (private element forwarding). Removed as not stated there: the cross-realm `instanceof` remark, the claim that JSON.stringify and Object.keys skip private fields, and the "protected-style accessors" advice.

Method: documentation only; no commands were run.
