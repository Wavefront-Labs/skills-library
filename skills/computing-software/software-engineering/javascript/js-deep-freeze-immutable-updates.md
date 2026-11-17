---
id: computing-software.software-engineering.javascript.js-deep-freeze-immutable-updates
name: js-deep-freeze-immutable-updates
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, immutable-updates, js-copying]
level: practitioner
status: docs-checked
description: "Update nested state immutably with spread, structural sharing, or Immer."
sources: ["https://immerjs.github.io/immer/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable update patterns

- Never change a property of an object, array or map; create an altered copy. By hand that means shallow-copying every affected level, for example `{ ...s, a: { ...s.a, b: v } }` or `arr.slice()` plus a replaced element.
- Structural sharing: unchanged parts of the tree are shared with the old version, so a reference that did not change means the object did not change (cheap change detection for React state, reducers, memoisation).
- For deep trees use Immer: `produce(state, draft => { draft.a.b = v; })`. The recipe mutates a draft (a proxy of the current state), Immer records the changes and builds the next state, and `produce` also freezes the data to guard against later accidental changes. Immer works with plain objects, arrays, Sets and Maps and throws on accidental mutation.

Self-check: unchanged sibling subtrees satisfy `next.x === prev.x`.

## Checked
2026-11-09. Confirmed against the Immer documentation introduction (immerjs.github.io/immer). Removed because that page does not state them: the `toSpliced` and `with` array methods, the `JSON.parse(JSON.stringify(x))` cloning caveat, `Object.freeze` being one level deep, and "freezes in development only".
Method: documentation only; no commands were run.
