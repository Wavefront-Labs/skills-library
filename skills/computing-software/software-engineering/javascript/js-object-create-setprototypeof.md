---
id: computing-software.software-engineering.javascript.js-object-create-setprototypeof
name: js-object-create-setprototypeof
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, object-create, js-prototypes]
level: practitioner
status: docs-checked
description: "Use Object.create with an optional descriptor map and null-prototype objects; prefer class syntax over prototype mutation."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object.create and prototypes

- `Object.create(proto, propertiesObject)`: the optional second argument maps keys to property descriptors, like `Object.defineProperties()`, so you can control enumerability and configurability, which object initializers cannot.
- `Object.create(null)` makes an object with `null` as its prototype; the object-initializer equivalent is `{ __proto__: null }`.
- MDN says `Object.create()` is believed to be faster than mutating the prototype with `Object.setPrototypeOf()`, but the difference is negligible if no instances exist yet and property accesses have not been optimized. Create with the right prototype rather than mutating later.
- Caveats include re-adding the `constructor` property for proper semantics; in modern code, class syntax should be preferred.

## Checked

Date: 2026-11-03. Confirmed on MDN Object/create: signature and propertiesObject, null prototype and `__proto__: null`, the performance remark, the constructor caveat, class preference. Removed as not stated there: the `__proto__`/`toString` collision claim, hasOwnProperty absence, getPrototypeOf advice, Object.hasOwn, for...in and Object.keys notes, Map-as-dictionary advice, and the Node print format self-check.

Method: documentation only; no commands were run.
