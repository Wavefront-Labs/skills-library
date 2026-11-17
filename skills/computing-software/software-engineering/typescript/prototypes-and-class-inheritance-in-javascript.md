---
id: computing-software.software-engineering.typescript.prototypes-and-class-inheritance-in-javascript
name: prototypes-and-class-inheritance-in-javascript
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, prototypes, prototype-chain, es-classes, instanceof, object-create, prototype-pollution]
level: practitioner
status: docs-checked
description: "Understand JavaScript's prototype chain under class syntax: property lookup, Object.create, instanceof across realms, extending built-ins, and prototype pollution."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_elements
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn
  - https://nodejs.org/api/cli.html#--disable-protomode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototypes and class inheritance in JavaScript

**Goal:** predict what `class`, `extends`, `instanceof` and property access actually do,
and avoid prototype-related security bugs.

## The chain
Every object has an internal `[[Prototype]]`. Property reads walk the chain until found;
writes create an own property on the object itself (unless a setter exists up the chain).
```js
const base = { greet() { return `hi ${this.name}`; } };
const o = Object.create(base);         // o.[[Prototype]] === base
o.name = "Ada";
o.greet();                             // found on base, `this` is o
Object.getPrototypeOf(o) === base;     // true
Object.hasOwn(o, "greet");             // false
```

## class is sugar over prototypes
```js
class Animal {
  #id = crypto.randomUUID();          // true private, per instance
  static count = 0;
  constructor(name) { this.name = name; Animal.count++; }
  speak() { return `${this.name} makes a sound`; }       // on Animal.prototype, shared
}
class Dog extends Animal {
  speak() { return `${super.speak()} - woof`; }
}
Object.getPrototypeOf(Dog.prototype) === Animal.prototype;   // true
Object.getPrototypeOf(Dog) === Animal;                       // statics inherit too
```
Differences from old constructor functions: the class body runs in strict mode and
class declarations behave as if not hoisted (like `let`/`const`).

## instanceof pitfalls
`x instanceof C` checks whether `C.prototype` is on x's chain. Fails across realms (for example
frames and windows). Use `Array.isArray`, brand checks
(`#field in obj`), or duck typing / `Symbol.for` tags for cross-boundary checks.

## Extending built-ins
Set `this.name` on custom errors for readable stack traces and pass `cause`.

## Prototype pollution
Merging untrusted JSON into objects can write to `Object.prototype`:
```js
merge({}, JSON.parse('{"__proto__": {"isAdmin": true}}'));
({}).isAdmin;     // true for every object in the process
```
Defences: validate input schemas (reject `__proto__`, `constructor`, `prototype` keys), use
`Object.create(null)` or `Map` for dictionaries, Node `--disable-proto=throw` (it only disables the `__proto__` accessor), and patched versions of merge utilities.

## Composition over inheritance
Deep class hierarchies are brittle in JS too; prefer small classes plus functions/objects
composed together, and keep inheritance to one level for framework base classes.

## Verify
- [ ] No deep-merge of untrusted input without key filtering.
- [ ] Cross-realm/package type checks don't rely on `instanceof`.

## Checked
Checked 2026-10-25 against the MDN content repository and the Node.js CLI docs. Confirmed: class bodies run in strict mode and class declarations behave as if not hoisted; `instanceof` and multiple realms; `Object.hasOwn`; private `#` elements and the `in` operator accepting a private identifier; `--disable-proto=mode` with `delete` and `throw` modes disabling `Object.prototype.__proto__`. Removed unconfirmed claims about must-call-with-new, non-enumerable methods, vm and worker realm failures, ES5 Error subclassing and freezing Object.prototype.
Method: documentation only; no commands were run.
