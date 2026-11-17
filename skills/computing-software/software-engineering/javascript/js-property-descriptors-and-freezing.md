---
id: computing-software.software-engineering.javascript.js-property-descriptors-and-freezing
name: js-property-descriptors-and-freezing
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-property-descriptors, object-defineproperty, object-freeze, enumerability]
level: advanced
status: docs-checked
description: "Define properties with Object.defineProperty descriptors; know descriptor defaults, data versus accessor, and non-configurable rules."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Property descriptors

- A descriptor is a data descriptor (`value`, `writable`) or an accessor descriptor (`get`, `set`), never both: mixing them throws `TypeError`. A descriptor with none of `value`, `writable`, `get` or `set` is treated as a data descriptor.
- Both kinds share `enumerable` and `configurable`. With `Object.defineProperty()` omitted flags default to `false`; creating a property by plain assignment makes it enumerable. Descriptor attributes are also read from the descriptor object's prototype chain, so specify everything explicitly or use a null-prototype descriptor object.
- Writing to a non-writable property does not change it and results in an error in strict mode.
- A non-configurable property's other attributes cannot be changed; if it is a writable data property its value can change and `writable` can go from `true` to `false`. A non-configurable, non-writable property cannot be modified at all.
- `Object.seal()` prevents extensions and makes every existing property non-configurable, so the set of properties is fixed while writable values can still change.
- `Object.getOwnPropertyDescriptor()` is the matching read method.

## Checked

Date: 2026-11-03. Confirmed on MDN Object/defineProperty (descriptor kinds, TypeError on mixing, defaults and inheritance caveat, assignment default, non-writable and non-configurable behaviour) and Object/seal. Removed as not covered by the pages read: freeze semantics, the Object.keys/entries/assign/spread and for...in enumeration claims, the Object.hasOwn versus hasOwnProperty advice, the Proxy invariant remark, and the getOwnPropertyDescriptor signature.

Method: documentation only; no commands were run.
