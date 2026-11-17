---
id: computing-software.web-development.frontend-development.javascript-private-fields-and-static-blocks
name: javascript-private-fields-and-static-blocks
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-classes, private-class-fields, class-static-blocks, javascript, es2022, accessors]
level: practitioner
status: docs-checked
description: "Using #private fields and methods, static initialisation blocks, getters/setters and the `#x in obj` brand check in JavaScript classes, with proxy and subclassing caveats."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_elements
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Static_initialization_blocks
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private fields, static blocks and accessors

## 1. Syntax
```js
class Account {
  static #count = 0;
  static #registry;
  static { Account.#registry = new Map(); }          // runs once at class definition

  #balance = 0;                                      // per-instance, truly private
  constructor(id) { this.id = id; Account.#count++; Account.#registry.set(id, this); }

  get balance() { return this.#balance; }            // read-only public view
  deposit(n) { this.#assertPositive(n); this.#balance += n; }
  #assertPositive(n) { if (!(n > 0)) throw new RangeError("amount must be > 0"); }

  static isAccount(o) { return #balance in o; }      // brand check, no throw
}
```

## 2. Semantics that surprise
- Private names are lexically scoped to the class body: no `obj["#x"]`; they are not properties and are not part of prototypal inheritance.
- Accessing `#x` on an object without it throws `TypeError` - use `#x in obj` to test.
- Subclasses cannot read the parent's `#fields`; expose protected-ish access through methods.
- **Proxies break private access**: `new Proxy(instance, {}).deposit(1)` throws because `this` is the proxy, not the target (MDN: "No private field forwarding"). Do not wrap private-field classes in proxies.
- Field initialisers run before the constructor body (after `super()` in subclasses); arrow-function fields (`handle = () => {}`) create one function per instance.

## 3. Static blocks
Use for multi-statement static setup that needs access to private statics (`try/catch` around config parsing, sharing private access with a helper defined in the same scope).

## 4. Accessors
- Expensive getters run on every access - cache explicitly.

## Verify
Unit test: `Object.keys(new Account(1))` lacks `balance` (it is a getter on the prototype); `Account.isAccount({})` is false; deposit(-1) throws RangeError.

## Checked

2026-10-26. MDN private elements (access on an object without the element throws TypeError; `#x in obj` brand check; fields initialised before the constructor in a base class and right after `super()` in a subclass), static initialization blocks (evaluated in declaration order with static fields, with access to private statics) and the Proxy page's "No private field forwarding" section. Removed the unconfirmed debugger, structuredClone, Vue/MobX, TypeScript and getter-without-setter statements.

Method: documentation only; no commands were run.
