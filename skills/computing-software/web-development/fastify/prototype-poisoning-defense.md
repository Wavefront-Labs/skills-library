---
id: computing-software.web-development.fastify.prototype-poisoning-defense
name: prototype-poisoning-defense
category: computing-software
field: web-development
product: fastify
tags: [fastify, security, prototype-poisoning, json, validation]
level: advanced
status: docs-checked
description: "Why __proto__ in JSON is dangerous and how Fastify's parser options and bourne-style scanning protect you."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Prototype-Poisoning.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`JSON.parse('{"b":5,"__proto__":{"c":6}}')` creates a harmless own property named `__proto__`. But `Object.assign({}, parsed)` copies it as a real prototype, so `x.c` is `6`. A validator that checks only own properties then misses attacker-supplied inherited data, which can pass through code that clones the parsed body before validation.

Defenses:
- Fastify parses JSON with secure-json-parse. `onProtoPoisoning` (for `__proto__`) and `onConstructorPoisoning` (for `constructor`) choose the action: `'error'` (default), `'remove'` or `'ignore'`.
- The original `bourne` approach: parse first, scan the raw text for the string `__proto__` only when present, then walk the object with a flat loop (not recursion, to avoid stack exhaustion on deep objects).
- v5 request `params` has no prototype, hardening against pollution.
- Query string: the Node default parser and `qs` were tested and are safe; a custom parser or base64 JSON in cookies needs care.

```js
const fastify = require('fastify')({ onProtoPoisoning: 'error' })
```

Costs: invalid JSON is already more expensive than valid JSON, so a poisoning check does not add a new DoS vector. Removing values was measured faster than throwing.

Gotcha: any solution that uses `JSON.parse()` on external data is potentially at risk. Inside custom JSON parsers use `fastify.getDefaultJsonParser(onProtoPoisoning, onConstructorPoisoning)`; `'ignore'` skips all validations, like calling `JSON.parse()` directly.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Prototype-Poisoning.md, Server.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: constructor.prototype (the option covers constructor), the claim that code outside Fastify bypasses the protections, and the invented Verify step.

Method: documentation only; no commands were run.
