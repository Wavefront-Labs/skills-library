---
id: computing-software.web-development.frontend-development.javascript-mixins-and-composition
name: javascript-mixins-and-composition
category: computing-software
field: web-development
product: frontend-development
tags: [class-mixins, composition-over-inheritance, javascript-classes, mixins, javascript]
level: practitioner
status: docs-checked
description: "Sharing behaviour across JavaScript classes with subclass-factory mixins or plain composition: when each fits, super chains, instanceof checks and avoiding deep hierarchies."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/hasInstance
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JavaScript mixins and composition over inheritance

JavaScript has single inheritance. When two unrelated classes need the same behaviour, pick composition first and reach for mixins only when the behaviour must hook into the class's own lifecycle (custom elements, framework base classes).

## 1. Composition (default)
```js
class Emitter { #h = new Map(); on(t, f) { (this.#h.get(t) ?? this.#h.set(t, new Set()).get(t)).add(f); }
  emit(t, d) { this.#h.get(t)?.forEach(f => f(d)); } }

class Cart {
  events = new Emitter();            // has-a, not is-a
  add(item) { /* ... */ this.events.emit("change", item); }
}
```
Testable in isolation, no name clashes, swappable. Prefer this for services, stores and anything without a shared lifecycle.

## 2. Subclass-factory mixins (when lifecycle matters)
```js
const Disposable = (Base) => class extends Base {
  #cleanups = [];
  addCleanup(fn) { this.#cleanups.push(fn); }
  disconnectedCallback() { super.disconnectedCallback?.(); this.#cleanups.splice(0).forEach(f => f()); }
};
const Focusable = (Base) => class extends Base { focus() { this.shadowRoot?.querySelector("[autofocus]")?.focus(); } };

class MyDialog extends Focusable(Disposable(HTMLElement)) {}
```
Rules:
- Always call `super.method?.()` so stacked mixins all run; order of application = order of `super` calls.
- Private `#fields` inside a mixin are per-mixin, so they never clash.
- `instanceof Disposable` does not work (it is a function returning a class). Add a `Symbol.hasInstance` or a brand symbol if you need checks.

## 3. Object.assign mixins (avoid for classes)
`Object.assign(Cart.prototype, emitterMethods)` copies only own enumerable properties, so class methods (non-enumerable) are not copied, and it cannot carry private fields. Acceptable only for plain method bags.

## 4. Smells
- More than 2-3 levels of `extends` or mixins stacked 4+ deep: extract collaborators instead.
- A mixin that reads fields defined in another mixin: hidden coupling, make it explicit via constructor arguments.

## Verify
- [ ] Each mixin works applied alone and stacked in either order; lifecycle hooks fire once per mixin; behaviour shared without inheritance is covered by unit tests on the collaborator.

## Checked

2026-10-26. MDN `extends` (the right-hand side can be any expression returning a constructor, used for mixins), Symbol.hasInstance and Object.assign (copies only enumerable properties). Removed the unconfirmed TypeScript typing line.

Method: documentation only; no commands were run.
