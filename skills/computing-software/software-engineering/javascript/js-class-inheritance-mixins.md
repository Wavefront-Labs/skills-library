---
id: computing-software.software-engineering.javascript.js-class-inheritance-mixins
name: js-class-inheritance-mixins
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, class-mixins, js-prototypes]
level: advanced
status: docs-checked
description: "Extend classes with extends and super, compose behaviour with mixin functions, and prefer composition over subclassing built-ins."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class inheritance super and mixins

- `class ChildClass extends ParentClass {}`: the parent can be any expression that evaluates to a constructor (a class or a function) or `null`. It must be callable with `new` and have a `prototype` property, so bound functions and `Proxy` objects cannot be subclassed.
- In a derived constructor, `super(...)` must be called before `this` is used, or a `ReferenceError` is thrown. A derived constructor may only return an object or `undefined`, otherwise a `TypeError` is thrown.
- `extends` sets two prototype links: `Object.getPrototypeOf(ChildClass) === ParentClass` (static members are inherited) and `Object.getPrototypeOf(ChildClass.prototype) === ParentClass.prototype` (instance members).
- A class has a single superclass. For mix-ins, use a function that takes a superclass and returns a subclass: `const calculatorMixin = (Base) => class extends Base { calc() {} };` then `class Bar extends calculatorMixin(randomizerMixin(Foo)) {}`.
- Classes cannot extend plain (non-constructible) objects; use `Object.setPrototypeOf(Dog.prototype, Animal)` to inherit from a regular object.
- Subclassing built-ins (`Array`, `Promise`, `Map`) is possible, but MDN says the standard committee considers the mechanism over-engineered, with performance and security costs, and recommends composition. Overriding one method can change the behaviour of others (for example `Map.prototype.set` is called by the `Map()` constructor, so a `ReadOnlyMap extends Map` that throws in `set()` cannot be constructed).
- `Symbol.species` (a static getter) lets built-in copying methods such as `map()` return a chosen constructor instead of the subclass.
- Prefer composition: hold the other object as a private field and expose only the methods you want; inheritance couples you to every inherited behaviour, including methods added to the base class later, and can break the Liskov substitution principle.

Self-check: `Object.getPrototypeOf(Bar.prototype)` is the anonymous mixin class's prototype, and walking further reaches `Foo.prototype`.

## Checked

Confirmed on the MDN extends page: parent-class requirements, super-before-this, return rule for derived constructors, the two prototype links, mix-in pattern, extending plain objects, built-in subclassing warning, Symbol.species and the composition guidance. Removed: claims that `instanceof` cannot see mixins, `Symbol.hasInstance` brand checks, `super.method()` in object literals, non-enumerable class methods and the `toJSON` mixin example, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
