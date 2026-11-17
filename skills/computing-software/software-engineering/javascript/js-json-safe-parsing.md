---
id: computing-software.software-engineering.javascript.js-json-safe-parsing
name: js-json-safe-parsing
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, json-parse-errors, js-json]
level: practitioner
status: draft
description: "Parse untrusted JSON defensively: errors, size limits, __proto__ keys and schema validation."
sources: ["https://owasp.org/www-community/attacks/Prototype_pollution"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe JSON parsing and prototype safety

- `JSON.parse` throws `SyntaxError` on bad input; always wrap in try/catch and report position (message includes it in modern engines).
- `JSON.parse('{"__proto__": {"x":1}}')` creates an own property named `__proto__` (not a pollution by itself), but merging it with a naive `Object.assign`/deep-merge can pollute prototypes; use `Object.create(null)` targets or a safe merge.
- Validate shape after parsing (Ajv with JSON Schema, Zod, Valibot); do not trust types.
- Cap body size before parsing; deeply nested input can blow the stack.
- Large integers lose precision; keep IDs as strings.

Self-check: feed `{"__proto__":{"admin":true}}` through your merge and confirm `({}).admin` stays undefined.
