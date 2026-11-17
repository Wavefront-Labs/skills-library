---
id: computing-software.software-engineering.javascript.js-json-reviver-replacer
name: js-json-reviver-replacer
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, json-reviver, js-json]
level: practitioner
status: docs-checked
description: "Customise JSON.stringify and JSON.parse for Dates, BigInt, large numbers and omitted keys using replacer, toJSON and reviver."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON reviver replacer and toJSON

- `JSON.stringify(value, replacer, space)`: the replacer is a function or an array of strings and numbers. An array limits output to those property names. A `toJSON()` method on a value decides what is serialised in its place; `Date` has one that returns the same as `toISOString()`, so dates become ISO strings.
- A replacer function receives `(key, value)` with the holder as `this`; it is first called with the key `""` for the root. Returning `undefined`, a function or a symbol omits the property.
- `JSON.parse(text, reviver)`: the reviver is called as `(key, value, context)`, depth-first starting with the most nested properties and ending with the root (key `""`). If it returns `undefined` the property is deleted, so return every untransformed value as is.
- Numbers are already rounded to JavaScript numbers before the reviver runs. For primitives, `context.source` holds the original text, so `BigInt(context.source)` recovers a large integer. Alternatively send large numbers as strings.
- A `BigInt` makes `JSON.stringify` throw a `TypeError`. Provide `BigInt.prototype.toJSON` or a replacer returning a string (or `JSON.rawJSON(...)` to emit a JSON number).
- Omitted or changed: `undefined`, functions and symbols are omitted in objects and become `null` in arrays; `NaN` and `Infinity` become `null`; `Map` and `Set` become `{}` because only enumerable own properties are visited.
- Circular references throw a `TypeError`. Replace the cyclic reference with a serialisable value yourself; for a deep copy, `structuredClone()` supports cycles.
- To hide secrets use a replacer (or an array whitelist) rather than deleting keys from the live object.

Self-check: `JSON.parse(JSON.stringify({d: new Date(0)}))` gives a string, not a Date.

## Checked

Confirmed on the cited MDN pages (JSON, JSON.stringify, JSON.parse): replacer array and function behaviour, toJSON and Date, BigInt and circular TypeError, omitted and null-converted values, Map and Set output, reviver order and delete-on-undefined, context.source, rawJSON. Removed: the WeakSet replacer suggestion (the page only says to implement it yourself).

Method: docs-only read of cited pages, 2026-11-08
