---
id: computing-software.software-engineering.javascript.js-loop-choice-forin-forof
name: js-loop-choice-forin-forof
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, for-in-vs-for-of, js-control-flow]
level: intro
status: docs-checked
description: "Pick the right loop: for...in walks enumerable string keys incl. inherited; use own-key helpers or for...of instead."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for...in vs for...of and loop choice

- `for...in` iterates all enumerable string-keyed properties of an object, ignoring symbol keys, and includes enumerable properties inherited through the prototype chain. The loop variable receives each property name as a string.
- Built-in non-enumerable properties such as `Array`'s `indexOf()` or `Object`'s `toString()` are not visited.
- Order is well defined in modern ECMAScript: within each object of the prototype chain, non-negative integer keys come first in ascending order, then other string keys in order of property creation.
- Own properties only: use `Object.keys()` (enumerable own string properties), `Object.getOwnPropertyNames()` (also non-enumerable ones), or test inside the loop with `Object.hasOwn(obj, prop)`.
- On arrays, `for...in` returns all enumerable properties, including non-index and inherited ones, and the index as a string. Unlike `for...of` it uses property enumeration, not the array iterator; in sparse arrays `for...of` visits empty slots and `for...in` does not. MDN recommends a numeric `for` loop, `forEach()` or `for...of` for arrays.
- MDN notes that many style guides and linters discourage `for...in`; it is most practical for debugging an object's properties or for ad hoc key-value objects.
- Do not add, modify or remove properties during iteration other than the one being visited. Properties added to the current object are never visited; changes to the prototype chain, deletions and enumerability changes may behave differently across implementations.
- A property that is shadowed and non-enumerable on a nearer object hides same-named enumerable ones further up the chain.
- `break` and `continue` work inside `for...in` as in other loops.
- A `var` loop variable is not local to the loop; `const` works as long as it is not reassigned in the body.

Self-check: `for (const i in ["a"]) console.log(typeof i)` prints `"string"`.

## Checked

2026-11-08. Confirmed on MDN for...in: enumerable string keys with inheritance, ordering, own-property helpers, array behaviour, sparse arrays vs `for...of`, mutation during iteration, `var` scope. Removed the claims about `Object.entries`, `forEach` with `break`/`await`, `Promise.all`, labels in callbacks, and mutating arrays while iterating, none of which that page covers.

Method: docs-only read of cited pages, 2026-11-08
