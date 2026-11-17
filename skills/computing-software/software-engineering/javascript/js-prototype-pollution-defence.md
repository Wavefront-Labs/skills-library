---
id: computing-software.software-engineering.javascript.js-prototype-pollution-defence
name: js-prototype-pollution-defence
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, prototype-pollution, js-security]
level: advanced
status: docs-checked
description: "Defend against prototype pollution with Map/Set, null-prototype objects, frozen prototypes and the Node --disable-proto flag."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype pollution defence

- Prototype pollution lets attackers manipulate an application's JavaScript objects and properties, leading to unauthorised data access, privilege escalation and even remote code execution (OWASP). The `__proto__` and `constructor.prototype` property paths are the vectors the cheat sheet names.
- Prefer `new Set()` or `new Map()` over object literals for sets of allowed values and option bags.
- If you need an object, create it with `Object.create(null)` so it does not inherit from the Object prototype. As a last resort for object literals, use `{__proto__: null}`.
- `Object.freeze()` on built-in prototypes prevents adding or removing properties and makes existing data properties non-writable. It is shallow, and libraries that modify built-in prototypes can break, so test compatibility first.
- `Object.seal()` only prevents adding or removing properties and changing their configuration; existing writable values can still change. Do not rely on it.
- Node.js `--disable-proto=delete` removes `__proto__` entirely. OWASP calls it defence in depth: pollution through `constructor.prototype` is still possible.

Self-check: merge `JSON.parse('{"__proto__":{"p":1}}')` into `{}` with your helper; afterwards `({}).p` must be `undefined`.

## Checked

2026-11-08. Confirmed on the OWASP Prototype Pollution Prevention Cheat Sheet: impact, `Set`/`Map`, `Object.create(null)`, `{__proto__: null}`, freeze and seal semantics, `--disable-proto=delete`. Removed the key-skip list for merge helpers, `Object.hasOwn`, the lodash version number, `npm audit`, and JSON-schema `additionalProperties: false` advice, which the cheat sheet does not state.

Method: docs-only read of cited pages, 2026-11-08
