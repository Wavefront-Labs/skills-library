---
id: computing-software.software-engineering.javascript.js-getters-setters-defineproperty
name: js-getters-setters-defineproperty
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, object-defineproperty, js-property-descriptors]
level: practitioner
status: docs-checked
description: "Define data and accessor properties with Object.defineProperty and Object.create descriptors; know defaults and TypeError cases."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessors and Object.defineProperty

- `Object.defineProperty(o, "id", { value: 1, enumerable: false, writable: false, configurable: false })`; when the property does not exist, omitted descriptor fields get defaults (`false` for the flags).
- An accessor descriptor uses `get` and `set` functions; a descriptor that is both a data descriptor (`value`, `writable`) and an accessor descriptor makes `defineProperty` throw `TypeError`.
- Redefining a non-configurable property throws `TypeError`, except that a writable data property's value can change and `writable` can go from `true` to `false`.
- `Object.create(proto, propertiesObject)`: the second argument maps keys to property descriptors, like the second argument of `Object.defineProperties()`.

Self-check: `Object.defineProperty({}, "x", { value: 1, get() { return 1; } })` throws `TypeError`.

## Checked

Date: 2026-11-03. Confirmed on MDN Object/defineProperty (defaults, descriptor kinds, TypeError cases, non-configurable exceptions) and Object/create (propertiesObject). Removed as not stated there: accessors in object literals, Object.getOwnPropertyDescriptors cloning, the lazy-getter pattern, and the Object.keys/JSON.stringify self-check.

Method: documentation only; no commands were run.
