---
id: computing-software.software-engineering.javascript.js-seal-preventextensions
name: js-seal-preventextensions
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, object-seal, js-property-descriptors]
level: practitioner
status: docs-checked
description: "Use Object.seal to fix an object's property set; know strict versus sloppy failure and what stays writable."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seal and preventExtensions

- `Object.seal(obj)` is equivalent to preventing extensions and then making every existing property `configurable: false`. The set of properties is fixed; values of writable data properties can still change. It returns the same object.
- Unlike `Object.freeze()`, a sealed object's existing properties may still be changed if they are writable.
- Sealing also stops converting a data property to an accessor (or back): `Object.defineProperty` throws `TypeError`.
- Failed additions or deletions on a sealed object silently do nothing in sloppy mode and throw `TypeError` in strict mode. Additions through `Object.defineProperty` throw either way.
- The prototype chain is untouched, but because extensions are prevented, `[[Prototype]]` cannot be reassigned.
- Private elements are not properties and are unaffected by sealing.
- Passing a primitive to `Object.seal` returns it unchanged (ES2015 and later).
- Check with `Object.isSealed(obj)`; related methods are `Object.preventExtensions()`, `Object.isExtensible()`, `Object.freeze()` and `Object.isFrozen()`.

Self-check: after `Object.seal(obj)`, `delete obj.foo` throws `TypeError` inside a `"use strict"` function and does nothing outside it.

## Checked

Date: 2026-11-03. Confirmed on MDN Object/seal: equivalence to preventExtensions plus non-configurable, writable values, strict versus sloppy behaviour, defineProperty TypeError, prototype and private elements, primitive argument, isSealed and related methods. Removed as not stated there: the freeze and preventExtensions definitions, the deep-freeze recipe, typed array and frozen array claims, and the TypeScript remark.

Method: documentation only; no commands were run.
