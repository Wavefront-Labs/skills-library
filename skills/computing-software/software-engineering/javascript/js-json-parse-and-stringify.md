---
id: computing-software.software-engineering.javascript.js-json-parse-and-stringify
name: js-json-parse-and-stringify
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-json, json-stringify, json-parse, reviver]
level: practitioner
status: docs-checked
description: "Serialise and parse JSON safely, including toJSON, replacers, revivers and unsupported values."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON

- `JSON.stringify(value, replacer, space)`: a replacer array whitelists keys, a replacer function transforms values, `space` pretty-prints (`JSON.stringify(v, null, 2)`).
- `Infinity`, `NaN` and `null` all serialise as `null`. Circular references and `BigInt` values throw (a `BigInt.prototype.toJSON` can provide serialisation).
- `JSON.parse(text, reviver)`: the reviver transforms the parsed result; it throws SyntaxError on bad input, so wrap in try/catch at trust boundaries and validate the shape afterwards.
- `"__proto__"` keys behave differently in JSON than in object literals (see the MDN note "Object literal syntax vs. JSON"); merging parsed objects into others can still cause prototype pollution.
- Trailing commas are invalid JSON.

## Checked

Date: 2026-11-02. Confirmed on MDN (Global_Objects/JSON/stringify, Global_Objects/JSON/parse): stringify replacer/space, Infinity/NaN as null, circular and BigInt throws, parse reviver and SyntaxError, __proto__ note, trailing commas. Removed as not stated there: handling of undefined/functions/symbols, Date, Map/Set, reviver order, precision loss and context.source, structuredClone advice, comments/single quotes (not read).

Method: documentation only; no commands were run.
