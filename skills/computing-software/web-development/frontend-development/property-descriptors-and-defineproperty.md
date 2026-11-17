---
id: computing-software.web-development.frontend-development.property-descriptors-and-defineproperty
name: property-descriptors-and-defineproperty
category: computing-software
field: web-development
product: frontend-development
tags: [property-descriptors, object-defineproperty, enumerable, writable, configurable, javascript]
level: practitioner
status: verified
description: "Data vs accessor property descriptors, defineProperty defaults, enumerability effects on keys/JSON/spread, and preventExtensions vs seal vs freeze."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Enumerability_and_ownership_of_properties
  - https://tc39.es/ecma262/#sec-property-attributes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property descriptors

## 1. Two kinds
```js
Object.defineProperty(obj, "id",    { value: 42, writable: false, enumerable: true, configurable: false });
Object.defineProperty(obj, "label", { get() { return this._l; }, set(v) { this._l = v.trim(); }, enumerable: true });
Object.getOwnPropertyDescriptor(obj, "id");   // { value: 42, writable: false, enumerable: true, configurable: false }
Object.getOwnPropertyDescriptors(obj);         // all, incl. accessors
```
A descriptor has `value/writable` **or** `get/set`, never both (TypeError).
**defineProperty defaults are all `false`**; plain assignment `obj.x = 1` creates `true/true/true`.

## 2. What each flag does
| Flag | false means |
|---|---|
| writable | assignment ignored in sloppy mode, **TypeError in strict mode/modules/classes** |
| enumerable | hidden from `for...in`, `Object.keys/entries`, `JSON.stringify`, object spread, `Object.assign` |
| configurable | cannot delete, cannot change flags (except writable true->false) |

Class methods are non-enumerable, which is why `{...instance}` copies fields but not methods.

## 3. Lock levels
| | add props | delete | change values |
|---|---|---|---|
| `Object.preventExtensions` | no | yes | yes |
| `Object.seal` | no | no | yes |
| `Object.freeze` | no | no | no (shallow) |
Check with `Object.isExtensible/isSealed/isFrozen`.

## 4. Copying correctly
Spread/`Object.assign` invoke getters and copy the value. To copy accessors as accessors:
```js
const clone = Object.defineProperties({}, Object.getOwnPropertyDescriptors(src));
```
`structuredClone` drops getters, functions and prototypes.

## Gotchas
- Defining a property on a frozen object or non-extensible target throws even in sloppy mode via defineProperty.
- Inherited setters run on assignment: `obj.x = 1` may hit a setter up the prototype chain instead of creating an own prop; `defineProperty` always creates an own prop.

Run in Node 20 (ES module): `defineProperty` with only `value` gave `writable/enumerable/configurable: false`, plain assignment gave all `true`; mixing `value` and `get` threw `TypeError`; writing a non-writable property threw `TypeError`; `{...instance}` skipped the prototype method (non-enumerable) and non-enumerable own props were skipped by `Object.keys`, `JSON.stringify`, spread and `Object.assign`; deleting a non-configurable property and re-enabling `writable` threw `TypeError`; `defineProperties` + `getOwnPropertyDescriptors` kept the getter while spread produced the value `3`; `defineProperty` on a frozen object threw; assigning through an inherited setter created `_x` on the child and no own `x`.

## Verify
- [ ] Tests run as ES modules (strict) so silent write failures surface as TypeErrors.
